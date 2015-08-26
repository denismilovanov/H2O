----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.drop_access_tokens(
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.users_sessions
        SET access_token = NULL
        WHERE access_token_generated_at < now() - interval '1 hour';

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.drop_access_tokens(
) TO h2o_front;
