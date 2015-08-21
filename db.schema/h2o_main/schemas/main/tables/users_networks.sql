----------------------------------------------------------------------------
-- социальные аккаунты

CREATE TABLE main.users_networks (
    user_id integer REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    network_id integer NOT NULL,
    user_network_id bigint NOT NULL,
    access_token varchar,

    CONSTRAINT users_networks_pkey PRIMARY KEY (user_network_id, network_id)
);

