----------------------------------------------------------------------------
-- заявки на вывод

CREATE TABLE billing.withdrawal_requests (
    id bigint NOT NULL PRIMARY KEY DEFAULT nextval('billing.withdrawal_requests_id_seq'::regclass),

    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_uuid uuid NOT NULL,
    status billing.withdrawal_request_status NOT NULL DEFAULT 'awaiting',

    amount numeric(9,2) NOT NULL CHECK (amount > 0),
    currency main.currency NOT NULL DEFAULT 'usd',

    -- т/с
    created_at timestamptz NOT NULL DEFAULT now(),
    billed_at timestamptz NULL,

    -- через что будем выводить?
    provider billing.transaction_provider NULL,
    -- какую транзакцию мы сделали на стороне провайдера?
    provider_transaction_id varchar NULL UNIQUE,
    -- какую транзакцию мы сделали у себя в случае успеха?
    our_transaction_id bigint NULL REFERENCES billing.transactions (id) ON DELETE CASCADE ON UPDATE CASCADE,

    -- для пейпала персонально
    email varchar NULL,
    -- что мы отправляем еще?
    request_data jsonb NOT NULL,
    -- что нам ответили?
    response_data jsonb NULL,

    -- на будущее
    admin_id integer NULL
);

