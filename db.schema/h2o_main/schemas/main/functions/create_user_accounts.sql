----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.create_user_accounts(
    i_user_id integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    INSERT INTO main.users_accounts
        SELECT  i_user_id, 'usd';

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.create_user_accounts(
    i_user_id integer
) TO h2o_front;
