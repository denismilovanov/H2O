----------------------------------------------------------------------------
-- пользователи в поколении

CREATE TABLE main.generations_users (
    generation_id integer NOT NULL,
    user_id integer NOT NULL,
    added_at timestamptz NOT NULL DEFAULT now(),

    CONSTRAINT generations_users_pkey PRIMARY KEY (generation_id, user_id)
);



