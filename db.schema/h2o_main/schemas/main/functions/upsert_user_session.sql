----------------------------------------------------------------------------
-- добавление или обновление сессии

CREATE OR REPLACE FUNCTION main.upsert_user_session(
    i_user_id integer,
    s_device_id varchar,
    t_device_type main.device_type,
    s_push_token varchar
)
    RETURNS record AS
$BODY$
DECLARE
    i_id bigint;
    s_access_token varchar := encode(gen_random_bytes(20), 'hex');
    s_refresh_token varchar := encode(gen_random_bytes(20), 'hex');
    r_result record;
BEGIN

    UPDATE main.users_sessions
        SET push_token = s_push_token,
            access_token = s_access_token,
            access_token_generated_at = now(),
            refresh_token = s_refresh_token,
            refresh_token_generated_at = now()
        WHERE   user_id = i_user_id AND
                device_id = s_device_id AND
                device_type = t_device_type
        RETURNING id, access_token, refresh_token INTO r_result;

    IF NOT FOUND THEN
        INSERT INTO main.users_sessions
            (user_id, device_id, device_type, push_token,
            access_token, refresh_token, access_token_generated_at, refresh_token_generated_at)
            VALUES (
                i_user_id,
                s_device_id,
                t_device_type,
                s_push_token,
                s_access_token,
                s_refresh_token,
                now(),
                now()
            )
            RETURNING id, access_token, refresh_token INTO r_result;
    END IF;

    RETURN r_result;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.upsert_user_session(
    i_user_id integer,
    s_device_id varchar,
    t_device_type main.device_type,
    s_push_token varchar
) TO h2o_user;
