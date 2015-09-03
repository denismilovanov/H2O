----------------------------------------------------------------------------
-- устройства

CREATE TABLE main.users_devices (
    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    device_type main.device_type NOT NULL,
    push_token varchar NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),

    CONSTRAINT users_devices_pkey PRIMARY KEY(user_id, device_type, push_token)
);
