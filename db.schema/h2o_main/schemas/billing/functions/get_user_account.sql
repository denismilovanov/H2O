----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.get_user_account(
    i_user_id integer
)
    RETURNS billing.users_accounts AS
$BODY$
DECLARE
    r_user_account billing.users_accounts;
BEGIN

    SELECT * INTO r_user_account
        FROM billing.users_accounts
        WHERE   user_id = i_user_id AND
                currency = 'usd';

    RETURN r_user_account;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.get_user_account(
    i_user_id integer
) TO h2o_front;
