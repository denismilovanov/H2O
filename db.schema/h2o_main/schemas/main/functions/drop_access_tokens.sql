----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.drop_access_tokens(
    i_seconds integer DEFAULT 3600
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.users_sessions
        SET access_token = NULL
        WHERE access_token_generated_at < now() - interval '1 second' * i_seconds;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.drop_access_tokens(
    i_seconds integer
) TO h2o_front;
