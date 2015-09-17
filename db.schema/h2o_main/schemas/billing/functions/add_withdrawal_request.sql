----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.add_withdrawal_request(
    i_user_id integer,
    u_user_uuid uuid,
    n_amount numeric,
    t_currency main.currency,
    t_provider billing.transaction_provider,
    s_provider_transaction_id varchar,
    s_email varchar,
    j_data jsonb
)
    RETURNS bigint AS
$BODY$
DECLARE
    i_id bigint;
BEGIN

    BEGIN

        INSERT INTO billing.withdrawal_requests
            (user_id, user_uuid, amount, currency, provider, provider_transaction_id, email, request_data)
            VALUES (
                i_user_id,
                u_user_uuid,
                n_amount,
                t_currency,
                t_provider,
                s_provider_transaction_id,
                s_email,
                j_data
            )
            RETURNING id INTO i_id;

        RETURN i_id;

    EXCEPTION WHEN unique_violation THEN
        RETURN 0;
    END;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.add_withdrawal_request(
    i_user_id integer,
    u_user_uuid uuid,
    n_amount numeric,
    t_currency main.currency,
    t_provider billing.transaction_provider,
    s_provider_transaction_id varchar,
    s_email varchar,
    j_data jsonb
) TO h2o_front;

