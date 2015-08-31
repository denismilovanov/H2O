----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.drop_all_tokens_by_access_token(
    s_access_token varchar
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    DELETE FROM main.users_sessions
        WHERE access_token = s_access_token;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.drop_all_tokens_by_access_token(
    s_access_token varchar
) TO h2o_front;
