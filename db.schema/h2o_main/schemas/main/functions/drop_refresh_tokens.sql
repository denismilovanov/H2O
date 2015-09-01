----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.drop_refresh_tokens(
    i_seconds integer DEFAULT 86400
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    DELETE FROM main.users_sessions
        WHERE refresh_token_generated_at < now() - interval '1 second' * i_seconds;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.drop_refresh_tokens(
    i_seconds integer
) TO h2o_front;
