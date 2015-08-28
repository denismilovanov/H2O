----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.add_transaction(
    i_user_id integer,
    u_user_uuid uuid,
    i_counter_user_id integer,
    u_counter_user_uuid uuid,
    t_direction main.transaction_direction,
    n_amount numeric,
    t_currency main.currency
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    INSERT INTO main.transactions
        (user_id, user_uuid, counter_user_id, counter_user_uuid,
        amount, currency, direction, status)
        VALUES (
            i_user_id,
            u_user_uuid,
            i_counter_user_id,
            u_counter_user_uuid,
            n_amount,
            t_currency,
            t_direction,
            'success'
        );

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.add_transaction(
    i_user_id integer,
    u_user_uuid uuid,
    i_counter_user_id integer,
    u_counter_user_uuid uuid,
    t_direction main.transaction_direction,
    n_amount numeric,
    t_currency main.currency
) TO h2o_front;

