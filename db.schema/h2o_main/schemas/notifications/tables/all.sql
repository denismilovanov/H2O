----------------------------------------------------------------------------
-- уведомления

CREATE TABLE notifications.all(
    id bigint NOT NULL PRIMARY KEY DEFAULT nextval('notifications.all_id_seq'::regclass),
    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    type notifications.type NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    data jsonb NOT NULL
);

