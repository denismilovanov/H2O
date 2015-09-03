----------------------------------------------------------------------------
-- добавление

CREATE OR REPLACE FUNCTION notifications.add_notification(
    i_user_id integer,
    t_notification_type notifications.type,
    j_data jsonb,
    i_counter_user_id integer
)
    RETURNS bigint AS
$BODY$
DECLARE
    i_id bigint;
BEGIN

    INSERT INTO notifications.all
        (user_id, type, data, counter_user_id)
        VALUES (
            i_user_id,
            t_notification_type,
            j_data,
            i_counter_user_id
        )
        RETURNING id INTO i_id;

    RETURN i_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION notifications.add_notification(
    i_user_id integer,
    t_notification_type notifications.type,
    j_data jsonb,
    i_counter_user_id integer
) TO h2o_front;
