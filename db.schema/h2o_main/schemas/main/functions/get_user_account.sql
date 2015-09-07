----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_user_account(
    i_user_id integer
)
    RETURNS main.users_accounts AS
$BODY$
DECLARE
    r_user_account main.users_accounts;
BEGIN

    SELECT * INTO r_user_account
        FROM main.users_accounts
        WHERE   user_id = i_user_id AND
                currency = 'usd';

    RETURN r_user_account;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_account(
    i_user_id integer
) TO h2o_front;
