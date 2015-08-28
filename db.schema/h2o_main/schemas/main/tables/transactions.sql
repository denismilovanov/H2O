----------------------------------------------------------------------------
-- транзакции

CREATE TABLE main.transactions (
    id bigint NOT NULL PRIMARY KEY DEFAULT nextval('main.transactions_id_seq'::regclass),

    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_uuid uuid NOT NULL,
    counter_user_id integer NOT NULL,
    counter_user_uuid uuid NOT NULL,
    direction main.transaction_direction NOT NULL,

    amount numeric(9,2) NOT NULL CHECK (amount > 0),
    currency main.currency NOT NULL DEFAULT 'usd',

    status main.transaction_status NOT NULL,
    is_anonymous boolean NOT NULL DEFAULT FALSE,

    created_at timestamptz NOT NULL DEFAULT now()
);


