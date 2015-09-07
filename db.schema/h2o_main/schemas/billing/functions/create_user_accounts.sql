----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.create_user_accounts(
    i_user_id integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    INSERT INTO billing.users_accounts
        SELECT  i_user_id, 'usd';

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.create_user_accounts(
    i_user_id integer
) TO h2o_front;
