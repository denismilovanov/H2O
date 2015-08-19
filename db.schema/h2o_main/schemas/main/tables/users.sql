----------------------------------------------------------------------------
-- пользователи

CREATE TABLE main.users (
    id integer NOT NULL DEFAULT nextval('main.users_id_seq'::regclass) PRIMARY KEY,
    uuid uuid NOT NULL UNIQUE DEFAULT public.uuid_generate_v4(),

    first_name varchar(100) NOT NULL,
    last_name varchar(100) NOT NULL,

    registered_at timestamptz NOT NULL DEFAULT now(),
    invite_code varchar(8) NOT NULL -- REFERENCES main.invite_codes (code)
);



