----------------------------------------------------------------------------
-- добавление или обновление токена пушей

CREATE OR REPLACE FUNCTION main.upsert_user_push_token(
    i_user_id integer,
    t_device_type main.device_type,
    s_push_token varchar
)
    RETURNS void AS
$BODY$
DECLARE
    i_id bigint;
BEGIN

    IF s_push_token IS NULL THEN
        RETURN;
    END IF;

    UPDATE main.users_devices
        SET updated_at = now()
        WHERE   user_id = i_user_id AND
                device_type = t_device_type AND
                push_token = s_push_token;

    IF NOT FOUND THEN
        INSERT INTO main.users_devices
            (user_id, device_type, push_token)
            VALUES (
                i_user_id,
                t_device_type,
                s_push_token
            );
    END IF;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.upsert_user_push_token(
    i_user_id integer,
    t_device_type main.device_type,
    s_push_token varchar
) TO h2o_front;
