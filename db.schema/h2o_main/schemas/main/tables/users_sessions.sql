----------------------------------------------------------------------------
-- сессии

CREATE TABLE main.users_sessions (
    user_id integer NOT NULL PRIMARY KEY REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    access_token varchar(64) NULL UNIQUE,
    refresh_token varchar(64) NULL UNIQUE,
    access_token_generated_at timestamptz NULL,
    refresh_token_generated_at timestamptz NULL
);



