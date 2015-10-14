# coding: utf-8

'''
    Usage: fab test deploy:front
    (do it from host machine, not vagrant)
'''

import os
from fabric.api import run, env, cd, roles, task, warn
from fabric.contrib import files
from fabric.contrib.project import rsync_project
from os import path, environ
from datetime import datetime
from fabric.operations import _prefix_commands, _prefix_env_vars, require
from fabric.contrib.console import confirm

HOSTS = {
    'production': ['94.75.248.180'],
    'test': ['94.75.248.180'],
}

GLOBAL = {
    'python': '/usr/bin/python',
    'source_copy': ['*'],
    'project_root': '$HOME/',
    'releases_dir': '$HOME/releases',
    'release_dir_new': '$HOME/releases/' + datetime.now().strftime('%Y%m%d%H%M%S'),
    'release_dir_current': '$HOME/releases/current',
    'source_dir': '$HOME/releases/source',
    'persistent_data_dir': '$HOME/releases/data',
    'releases_limit': 3,
    'persistent_data': {}
}

SERVICES = {

    'front': {
        'test': {
            'user': 'h2o_front_test',
            'source_branch': 'develop',
            'hosts': HOSTS['test'],
            'host_string': HOSTS['test'][0],
            'reload_commands': [
                '/usr/bin/uwsgi --reload /tmp/h2o_front_test.pid',
            ],
        },
        'production': {
            'user': 'h2o_front',
            'source_branch': 'master',
            'hosts': HOSTS['production'],
            'host_string': HOSTS['production'][0],
            'reload_commands': [
                '/usr/bin/uwsgi --reload /tmp/h2o_front_prod.pid',
            ],
        },
    },

    'admin': {
        'production': {
            'user': 'h2o_admin',
            'source_branch': 'develop-future',
            'hosts': HOSTS['production'],
            'host_string': HOSTS['production'][0],
            'reload_commands': [
                '/usr/bin/uwsgi --reload /tmp/h2o_admin_prod.pid',
            ],
        },
    },

    'daemons': {
        'test': {
            'user': 'h2o_daemons_test',
            'source_branch': 'develop',
            'hosts': HOSTS['test'],
            'host_string': HOSTS['test'][0],
            'reload_commands': [
                'if [ -f /tmp/h2o_daemons_test_circus.pid ]; then cat /tmp/h2o_daemons_test_circus.pid | xargs kill ; fi',
                'circusd circus.ini --pidfile /tmp/h2o_daemons_test_circus.pid --daemon',
            ],
        },
        'production': {
            'user': 'h2o_daemons',
            'source_branch': 'master',
            'hosts': HOSTS['production'],
            'host_string': HOSTS['production'][0],
            'reload_commands': [
                'if [ -f /tmp/h2o_daemons_prod_circus.pid ]; then cat /tmp/h2o_daemons_prod_circus.pid | xargs kill ; fi',
                'circusd circus.ini --pidfile /tmp/h2o_daemons_prod_circus.pid --daemon',
            ],
        },
    },

}

'''
Загрузка настроек в зависимости от указанного сервиса и его окружения
'''
def get_settings(service, stage):
    if service not in SERVICES:
        raise Exception('Несуществующий сервис: ' + service)
    if stage not in SERVICES[service]:
        raise Exception('Настройки окружения ' + stage + ' отсутствуют у сервиса ' + service)
    settings = {}
    # Загрузка глобальных настроек
    for option, value in GLOBAL.items():
        settings[option] = value
    # Загрузка глобальных настроек на уровне сервиса
    # Затем локальные
    for option, value in SERVICES[service][stage].items():
        settings[option] = value
    return settings


def set_env_settings(service):
    # Загружаем настройки окружения
    settings = get_settings(service, env.stage)
    # Устанавливаем настройки окружения
    for option, value in settings.items():
        setattr(env, option, value)


@task
def production():
    stage_set('production')

@task
def test():
    stage_set('test')

def stage_set(stage_name='test'):
    env.stage = stage_name

@task
def deploy(service_name, branch=None):
    require('stage', provided_by=(test,production,))

    set_env_settings(service_name)

    if branch is not None:
        env.source_branch = branch

    # Выполняем деплой
    with cd(env.project_root):
        run('uname -a && date')
        git_prefix = 'git --git-dir={0}/.git --work-tree={0}'.format(env.source_dir)

        # Если директории для релизов не существует – создаем ее и клонируем репозиторий
        if not files.exists(env.releases_dir, use_sudo=False, verbose=True):
            run('mkdir -p {}'.format(env.releases_dir))
            run('git clone {} {}'.format(env.repository, env.source_dir))

        # Получаем последние изменения из репозитория
        run('{git} fetch origin --prune'.format(git=git_prefix))
        run('{git} checkout {source_branch}'.format(git=git_prefix, source_branch=env.source_branch))
        run('{git} pull origin {source_branch}'.format(git=git_prefix, source_branch=env.source_branch))

    with cd(env.source_dir):
        run('git submodule update --init')

    with cd(env.project_root):
        # Создаем директорию для нового релиза и копируем туда исходные файлы
        run('mkdir -p {}'.format(env.release_dir_new))
        for source in env.source_copy:
            run('cp -r {}/{} {}'.format(env.source_dir, source, env.release_dir_new))

    with cd(env.release_dir_new):
        if service_name != 'admin':
            run('sudo /usr/local/bin/pip install -r requirements.txt')
        else:
            run('/home/h2o_admin/releases/env/bin/pip install -r requirements.txt')
            run('/home/h2o_admin/releases/env/bin/python manage.py migrate')
            run('mkdir static')
            run('/home/h2o_admin/releases/env/bin/python manage.py collectstatic --noinput')


    with cd(env.project_root):
        # При подтверждении делаем новый релиз текущим
        if confirm('Do you want change release to "{}"?'.format(env.release_dir_new), default=False):
            run('ln -sfn {} {}'.format(env.release_dir_new, env.release_dir_current))
            print('Released "{}"'.format(env.release_dir_new))
        else:
            warn('Release "{}" was canceled'.format(env.release_dir_new))
            run('rm -rf {}'.format(env.release_dir_new))
            return

        # Сохраняем ссылку на предыдущий релиз
        run('readlink -f {} >> {}/releases.txt'.format(env.release_dir_current, env.releases_dir))
        run('ln -sfn {} {}'.format(env.release_dir_new, env.release_dir_current))

        # Удаляем старые релизы
        releases_limit = env.releases_limit if 'releases_limit' in env else 3
        run('head -n -{0} {1}/releases.txt | xargs rm -rf'.format(releases_limit, env.releases_dir))
        run('tail -n -{0} {1}/releases.txt > {1}/temp.txt && mv {1}/temp.txt {1}/releases.txt'.format(releases_limit, env.releases_dir))


    for cmd in env.reload_commands:
        run(cmd)


