----------------------------------------------------------------------------
-- за кем пользователь следит

CREATE TABLE main.users_follows (
    user_id integer REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    follow_user_id integer REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    followed_since timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT users_follows_pkey PRIMARY KEY (user_id, follow_user_id)
);


