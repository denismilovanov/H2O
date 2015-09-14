----------------------------------------------------------------------------
-- пользователи

CREATE TABLE main.users (
    id integer PRIMARY KEY,
    uuid uuid NOT NULL UNIQUE,
    name varchar(255) NOT NULL,
    registered_at timestamptz NOT NULL DEFAULT now(),
    status main.user_status NOT NULL DEFAULT 'i_have_enough_money',
    visibility main.user_visibility NOT NULL DEFAULT 'visible_for_all',
    avatar_url varchar NULL,
    is_deleted boolean NOT NULL DEFAULT FALSE,
    facebook_id bigint NOT NULL,
    generation integer NOT NULL,
    num_in_generation integer NOT NULL
);

CREATE UNIQUE INDEX users_facebook_id_ukey
    ON main.users
    USING btree(facebook_id)
    WHERE id > 0;

CREATE UNIQUE INDEX users_generations_ukey
    ON main.users
    USING btree(generation, num_in_generation);


