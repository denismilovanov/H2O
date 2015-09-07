----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.add_transaction(
    i_user_id integer,
    u_user_uuid uuid,
    i_counter_user_id integer,
    u_counter_user_uuid uuid,
    t_direction billing.transaction_direction,
    n_amount numeric,
    t_currency main.currency,
    b_is_anonymous boolean
)
    RETURNS bigint AS
$BODY$
DECLARE
    i_id bigint;
BEGIN

    INSERT INTO billing.transactions
        (user_id, user_uuid, counter_user_id, counter_user_uuid,
        amount, currency, direction, status, is_anonymous)
        VALUES (
            i_user_id,
            u_user_uuid,
            i_counter_user_id,
            u_counter_user_uuid,
            n_amount,
            t_currency,
            t_direction,
            'success',
            b_is_anonymous
        )
        RETURNING id INTO i_id;

    RETURN i_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.add_transaction(
    i_user_id integer,
    u_user_uuid uuid,
    i_counter_user_id integer,
    u_counter_user_uuid uuid,
    t_direction billing.transaction_direction,
    n_amount numeric,
    t_currency main.currency,
    b_is_anonymous boolean
) TO h2o_front;

