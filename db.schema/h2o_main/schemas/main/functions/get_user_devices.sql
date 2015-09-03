----------------------------------------------------------------------------
-- список пуш-токенов и устройств

CREATE OR REPLACE FUNCTION main.get_user_devices(
    i_user_id integer
)
    RETURNS SETOF main.user_device AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY    WITH tokens AS (
                        SELECT device_type, push_token
                            FROM main.users_devices
                            WHERE   user_id = i_user_id AND
                                    push_token IS NOT NULL
                            ORDER BY updated_at DESC
                            LIMIT 10
                    )
                    SELECT DISTINCT device_type, push_token
                        FROM tokens;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_devices(
    i_user_id integer
) TO h2o_front;
