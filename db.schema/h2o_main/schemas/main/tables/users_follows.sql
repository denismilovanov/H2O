----------------------------------------------------------------------------
-- за кем пользователь следит

CREATE TABLE main.users_follows (
    id integer DEFAULT nextval('main.users_follows_id_seq') PRIMARY KEY,
    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    follow_user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    followed_since timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT users_follows_ukey UNIQUE (user_id, follow_user_id)
);

ALTER TABLE main.users_follows
    ADD CONSTRAINT users_follows_not_equal
    CHECK (user_id != follow_user_id);
