----------------------------------------------------------------------------
-- обновление токена

CREATE OR REPLACE FUNCTION main.get_refresh_token(
    s_user_uuid uuid,
    b_drop boolean DEFAULT FALSE
)
    RETURNS varchar AS
$BODY$
DECLARE
    s_refresh_token varchar;
BEGIN

    IF NOT b_drop THEN
        s_refresh_token := encode(gen_random_bytes(20), 'hex');
    END IF;

    UPDATE main.users_sessions
        SET refresh_token = s_refresh_token,
            refresh_token_generated_at = now()
        WHERE user_id = (SELECT id FROM main.get_user_by_uuid(s_user_uuid));

    RETURN s_refresh_token;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_refresh_token(
    s_user_uuid uuid,
    b_drop boolean
) TO h2o_user;
