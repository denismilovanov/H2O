----------------------------------------------------------------------------
-- приглашения

CREATE TABLE main.invite_codes (
    invite_code varchar(40) PRIMARY KEY,
    owner_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    is_used boolean NOT NULL DEFAULT FALSE,
    invited_user_id integer NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    status main.invite_code_status NOT NULL DEFAULT 'free',
    created_at timestamptz NOT NULL DEFAULT now(),
    used_at timestamptz NULL,
    email varchar NULL,
    entrance_gift boolean NULL
);

CREATE UNIQUE INDEX invite_codes_email_ukey
    ON main.invite_codes
    USING btree(lower(email));

-- батч
ALTER TABLE main.invite_codes
    ADD COLUMN batch integer NULL;

ALTER TABLE main.invite_codes
    ADD COLUMN invited_at timestamptz NULL;
