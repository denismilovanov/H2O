----------------------------------------------------------------------------
-- удаление токена пушей

CREATE OR REPLACE FUNCTION main.delete_user_push_token(
    i_user_id integer,
    s_push_token varchar
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    DELETE FROM main.users_devices
        WHERE   -- user_id = i_user_id AND
                device_type IN ('ios', 'android') AND
                push_token = s_push_token;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.delete_user_push_token(
    i_user_id integer,
    s_push_token varchar
) TO h2o_front;
