----------------------------------------------------------------------------
-- статистика

CREATE TABLE statistics.overall (
    user_id integer PRIMARY KEY REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,

    supports_transactions_count integer DEFAULT 0,
    supports_users_count integer DEFAULT 0,
    supports_users_ids integer[] DEFAULT array[]::integer[],

    receives_transactions_count integer DEFAULT 0,
    receives_users_count integer DEFAULT 0,
    receives_users_ids integer[] DEFAULT array[]::integer[]
);



