----------------------------------------------------------------------------
-- статистика

CREATE TABLE statistics.counter_users (
    id integer DEFAULT nextval('statistics.counter_users_id_seq') PRIMARY KEY,

    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    counter_user_id integer NOT NULL, -- 0 для анонимных поступлений
    transaction_direction billing.transaction_direction NOT NULL,

    transactions_count integer NOT NULL DEFAULT 0,
    transactions_amount_sum numeric(15,2) NOT NULL DEFAULT 0,

    CONSTRAINT counter_users_ukey UNIQUE (user_id, counter_user_id, transaction_direction)
);



