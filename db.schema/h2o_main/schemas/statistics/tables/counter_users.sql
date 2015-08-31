----------------------------------------------------------------------------
-- статистика

CREATE TABLE statistics.counter_users (
    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    counter_user_id integer NOT NULL,
    transaction_direction main.transaction_direction NOT NULL,

    transactions_count integer NOT NULL DEFAULT 0,
    amount_sum numeric(15,2) NOT NULL DEFAULT 0,

    CONSTRAINT counter_users_pkey PRIMARY KEY(user_id, counter_user_id, transaction_direction)
);



