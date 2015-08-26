----------------------------------------------------------------------------
-- обновление токена

CREATE OR REPLACE FUNCTION main.get_access_token(
    s_user_uuid uuid,
    b_drop boolean DEFAULT FALSE
)
    RETURNS varchar AS
$BODY$
DECLARE
    s_access_token varchar;
BEGIN

    IF NOT b_drop THEN
        s_access_token := encode(gen_random_bytes(20), 'hex');
    END IF;

    UPDATE main.users_sessions
        SET access_token = s_access_token,
            access_token_generated_at = now()
        WHERE user_id = (SELECT id FROM main.get_user_by_uuid(s_user_uuid));

    RETURN s_access_token;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_access_token(
    s_user_uuid uuid,
    b_drop boolean
) TO h2o_front;
