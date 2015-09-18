----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.update_user_balance(
    i_user_id integer,
    n_amount numeric,
    n_hold_amount numeric,
    t_currency main.currency
)
    RETURNS numeric AS
$BODY$
DECLARE
    n_balance numeric;
BEGIN

    n_hold_amount := coalesce(n_hold_amount, 0);
    n_amount := coalesce(n_amount, 0);

    UPDATE billing.users_accounts
        SET balance = balance + n_amount,
            hold = hold + n_hold_amount
        WHERE   user_id = i_user_id AND
                currency = 'usd'
        RETURNING balance INTO n_balance;

    RETURN n_balance;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.update_user_balance(
    i_user_id integer,
    n_amount numeric,
    n_hold_amount numeric,
    t_currency main.currency
) TO h2o_front;
