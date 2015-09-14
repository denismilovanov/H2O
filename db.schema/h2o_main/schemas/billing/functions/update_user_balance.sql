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
    n_balance numeric;
BEGIN

    UPDATE billing.users_accounts
        SET balance = balance + n_amount
        WHERE   user_id = i_user_id AND
                currency = 'usd'
        RETURNING balance INTO n_balance;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.update_user_balance(
    i_user_id integer,
    n_amount numeric,
    t_currency main.currency
) TO h2o_front;
