----------------------------------------------------------------------------
-- кто следит за пользователем

CREATE TABLE main.users_followed_by (
    user_id integer REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    followed_by_user_id integer REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    followed_since timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT users_followed_by_pkey PRIMARY KEY (user_id, followed_by_user_id)
);


