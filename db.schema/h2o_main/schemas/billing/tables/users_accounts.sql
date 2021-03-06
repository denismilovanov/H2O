----------------------------------------------------------------------------
-- совокупные счета

CREATE TABLE billing.users_accounts (
    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    currency main.currency NOT NULL DEFAULT 'usd',
    -- баланс, который можно вывести
    balance numeric(9,2) NOT NULL DEFAULT 0.0,
    -- замороженные деньги (холд)
    hold numeric(9,2) NOT NULL DEFAULT 0.0,

    CONSTRAINT users_accounts_pkey PRIMARY KEY (user_id, currency)
);

-- проверка на неотрицательность
ALTER TABLE billing.users_accounts
    ADD CONSTRAINT users_accounts_positive_check
    CHECK (
        CASE
            WHEN user_id > 0 THEN balance >= 0 AND hold >= 0
            ELSE TRUE
        END
    );
