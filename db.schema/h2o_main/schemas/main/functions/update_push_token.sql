----------------------------------------------------------------------------
-- обновление токена

CREATE OR REPLACE FUNCTION main.update_push_token(
    s_access_token varchar,
    s_push_token varchar
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.users_sessions
        SET push_token = s_push_token
        WHERE access_token = s_access_token;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.update_push_token(
    s_access_token varchar,
    s_push_token varchar
) TO h2o_front;
