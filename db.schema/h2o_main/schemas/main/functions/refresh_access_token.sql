----------------------------------------------------------------------------
-- обновление токена

CREATE OR REPLACE FUNCTION main.refresh_access_token(
    s_refresh_token varchar
)
    RETURNS varchar AS
$BODY$
DECLARE
    s_access_token varchar;
BEGIN

    s_access_token := encode(gen_random_bytes(20), 'hex');

    UPDATE main.users_sessions
        SET access_token = s_access_token
        WHERE refresh_token = s_refresh_token;

    IF NOT FOUND THEN
        s_access_token := NULL;
    END IF;

    RETURN s_access_token;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.refresh_access_token(
    s_refresh_token varchar
) TO h2o_front;
