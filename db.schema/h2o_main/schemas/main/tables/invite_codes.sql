----------------------------------------------------------------------------
-- приглашения

CREATE TABLE main.invite_codes (
    code varchar(8) PRIMARY KEY,
    owner_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    is_used boolean NOT NULL DEFAULT FALSE,
    invited_user_id integer NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE
);


