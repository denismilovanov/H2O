----------------------------------------------------------------------------
-- устройства

CREATE TABLE main.users_devices (
    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    device_type main.device_type NOT NULL,
    push_token varchar NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),

    CONSTRAINT users_devices_pkey PRIMARY KEY(user_id, device_type, push_token)
);

-- ограничения на длину токена
ALTER TABLE main.users_devices
    ADD CONSTRAINT token_length CHECK (
        CASE WHEN device_type = 'ios' AND push_token IS NOT NULL THEN length(push_token) = 64
             WHEN device_type = 'android' AND push_token IS NOT NULL THEN length(push_token) = 152
             ELSE TRUE
        END
    );
