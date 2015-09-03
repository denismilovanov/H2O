----------------------------------------------------------------------------
-- удаление

CREATE OR REPLACE FUNCTION notifications.get_notification(
    i_user_id integer,
    i_id bigint
)
    RETURNS notifications.all AS
$BODY$
DECLARE
    r_record notifications.all;
BEGIN

    SELECT * INTO r_record
        FROM notifications.all
        WHERE   id = i_id AND
                user_id = i_user_id;

    RETURN r_record;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION notifications.get_notification(
    i_user_id integer,
    i_id bigint
) TO h2o_front;
