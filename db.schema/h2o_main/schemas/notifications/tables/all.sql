----------------------------------------------------------------------------
-- уведомления

CREATE TABLE notifications.all(
    id bigint NOT NULL PRIMARY KEY DEFAULT nextval('notifications.all_id_seq'::regclass),
    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    type notifications.type NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    data jsonb NOT NULL,
    counter_user_id integer NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE
);

ALTER TABLE notifications.all
    ADD CONSTRAINT counter_user_id_check
    CHECK  (CASE WHEN type IN ('somebody_follows_me', 'somebody_sent_me_money')
                    THEN counter_user_id IS NOT NULL
                    ELSE counter_user_id IS NULL
            END);

CREATE INDEX all_user_id_idx
    ON notifications.all
    USING btree(user_id);

ALTER TABLE notifications.all
    ADD COLUMN is_read boolean NOT NULL DEFAULT FALSE;
