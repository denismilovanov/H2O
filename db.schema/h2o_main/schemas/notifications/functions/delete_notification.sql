----------------------------------------------------------------------------
-- удаление

CREATE OR REPLACE FUNCTION notifications.delete_notification(
    i_user_id integer,
    i_id bigint
)
    RETURNS boolean AS
$BODY$
DECLARE

BEGIN

    DELETE FROM notifications.all
        WHERE   id = i_id AND
                user_id = i_user_id;

    RETURN FOUND;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION notifications.delete_notification(
    i_user_id integer,
    i_id bigint
) TO h2o_front;
