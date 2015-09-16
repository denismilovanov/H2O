----------------------------------------------------------------------------
-- удаление всего

CREATE OR REPLACE FUNCTION notifications.delete_all_notifications_by_user_id(
    i_user_id integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    DELETE FROM notifications.all
        WHERE user_id = i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION notifications.delete_all_notifications_by_user_id(
    i_user_id integer
) TO h2o_front;
