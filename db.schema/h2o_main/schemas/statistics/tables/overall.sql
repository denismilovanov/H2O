----------------------------------------------------------------------------
-- статистика

CREATE TABLE statistics.overall (
    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    transaction_direction main.transaction_direction NOT NULL,

    transactions_count integer NOT NULL DEFAULT 0,
    users_count integer NOT NULL DEFAULT 0,
    transactions_amount_sum numeric(15,2) NOT NULL DEFAULT 0.0,

    CONSTRAINT overall_pkey PRIMARY KEY(user_id, transaction_direction)
);




