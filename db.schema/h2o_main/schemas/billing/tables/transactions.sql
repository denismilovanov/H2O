----------------------------------------------------------------------------
-- транзакции

CREATE TABLE billing.transactions (
    id bigint NOT NULL PRIMARY KEY DEFAULT nextval('billing.transactions_id_seq'::regclass),

    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_uuid uuid NOT NULL,
    counter_user_id integer NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    counter_user_uuid uuid NULL,
    direction billing.transaction_direction NOT NULL,

    amount numeric(9,2) NOT NULL CHECK (amount > 0),
    currency main.currency NOT NULL DEFAULT 'usd',

    status billing.transaction_status NOT NULL,
    is_anonymous boolean NOT NULL DEFAULT FALSE,

    created_at timestamptz NOT NULL DEFAULT now(),

    provider billing.transaction_provider NULL,
    provider_transaction_id varchar NULL UNIQUE
);


