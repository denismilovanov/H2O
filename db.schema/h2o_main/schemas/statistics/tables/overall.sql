----------------------------------------------------------------------------
-- статистика

CREATE TABLE statistics.overall (
    id integer DEFAULT nextval('statistics.overall_id_seq') PRIMARY KEY,

    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    transaction_direction billing.transaction_direction NOT NULL,

    transactions_count integer NOT NULL DEFAULT 0,
    users_count integer NOT NULL DEFAULT 0,
    transactions_amount_sum numeric(15,2) NOT NULL DEFAULT 0.0,

    CONSTRAINT overall_ukey UNIQUE (user_id, transaction_direction)
);





