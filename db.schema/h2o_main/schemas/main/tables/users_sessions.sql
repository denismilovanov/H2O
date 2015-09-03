----------------------------------------------------------------------------
-- сессии

CREATE TABLE main.users_sessions (
    id bigint NOT NULL PRIMARY KEY DEFAULT nextval('main.users_sessions_id_seq'::regclass),

    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    device_type main.device_type NOT NULL,

    access_token varchar(40) NULL UNIQUE,
    refresh_token varchar(40) NULL UNIQUE,
    access_token_generated_at timestamptz NULL,
    refresh_token_generated_at timestamptz NULL
);
