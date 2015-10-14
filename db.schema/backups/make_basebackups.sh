#!/bin/bash

# usage: crontab
# 0 * * * * sh /pg_backups/make_backups.sh >> /pg_backups/log.txt

DATE="$(date +"%Y")_$(date +"%m")_$(date +"%d")_$(date +"%H")"

mkdir /tmp/pg_backup
/usr/bin/pg_basebackup -U postgres -p 5433 -D /tmp/pg_backup -Ft -z -Xf
mv /tmp/pg_backup/base.tar.gz /pg_backups/test/base.${DATE}.tar.gz
rm -rf /tmp/pg_backup

mkdir /tmp/pg_backup
/usr/bin/pg_basebackup -U postgres -p 5432 -D /tmp/pg_backup -Ft -z -Xf
mv /tmp/pg_backup/base.tar.gz /pg_backups/production/base.${DATE}.tar.gz
rm -rf /tmp/pg_backup
