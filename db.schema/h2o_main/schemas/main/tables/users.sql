----------------------------------------------------------------------------
-- пользователи

CREATE TABLE main.users (
    id integer NOT NULL DEFAULT nextval('main.users_id_seq'::regclass) PRIMARY KEY,
    uuid uuid NOT NULL UNIQUE DEFAULT public.uuid_generate_v4(),
    name varchar(255) NOT NULL,
    registered_at timestamptz NOT NULL DEFAULT now(),
    status main.user_status NOT NULL DEFAULT 'i_do_not_need_money',
    visibility main.user_visibility NOT NULL DEFAULT 'visible',
    avatar_url varchar NULL
);


