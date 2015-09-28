----------------------------------------------------------------------------
-- получение числа непрочитанных

CREATE OR REPLACE FUNCTION notifications.get_unread_notifications_count(
    i_user_id integer
)
    RETURNS integer AS
$BODY$
DECLARE
    i_count integer;
BEGIN

    SELECT count(1) INTO i_count
        FROM notifications.all
        WHERE   user_id = i_user_id AND
                NOT is_read;

    RETURN i_count;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION notifications.get_unread_notifications_count(
    i_user_id integer
) TO h2o_front;
