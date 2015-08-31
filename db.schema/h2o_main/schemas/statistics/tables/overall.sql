----------------------------------------------------------------------------
-- статистика

CREATE TABLE statistics.overall (
    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    transaction_direction main.transaction_direction NOT NULL,

    transactions_count integer DEFAULT 0,
    users_count integer DEFAULT 0,
    users_ids integer[] DEFAULT array[]::integer[],

    CONSTRAINT overall_pkey PRIMARY KEY(user_id, transaction_direction)
);



