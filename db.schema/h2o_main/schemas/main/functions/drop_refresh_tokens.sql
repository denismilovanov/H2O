----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.drop_refresh_tokens(
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    DELETE FROM main.users_sessions
        WHERE refresh_token_generated_at < now() - interval '1 day';

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.drop_refresh_tokens(
) TO h2o_user;
