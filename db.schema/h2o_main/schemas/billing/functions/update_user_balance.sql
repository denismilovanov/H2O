----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.update_user_balance(
    i_user_id integer,
    n_amount numeric,
    t_currency main.currency
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE billing.users_accounts
        SET balance = balance + n_amount
        WHERE   user_id = i_user_id AND
                currency = 'usd';

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.update_user_balance(
    i_user_id integer,
    n_amount numeric,
    t_currency main.currency
) TO h2o_front;
