----------------------------------------------------------------------------
-- отметка всего как прочитанного

CREATE OR REPLACE FUNCTION notifications.read_all_notifications(
    i_user_id integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE notifications.all
        SET is_read = TRUE
        WHERE   user_id = i_user_id AND
                NOT is_read;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION notifications.read_all_notifications(
    i_user_id integer
) TO h2o_front;
