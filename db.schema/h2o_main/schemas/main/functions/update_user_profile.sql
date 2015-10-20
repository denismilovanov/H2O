----------------------------------------------------------------------------
-- обновление профиля

CREATE OR REPLACE FUNCTION main.update_user_profile(
    i_user_id integer,
    t_visibility main.user_visibility,
    t_status main.user_status,
    b_push_notifications boolean
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.users
        SET status = COALESCE(t_status, status),
            visibility = COALESCE(t_visibility, visibility),
            push_notifications = b_push_notifications
        WHERE id = i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.update_user_profile(
    i_user_id integer,
    t_visibility main.user_visibility,
    t_status main.user_status,
    b_push_notifications boolean
) TO h2o_front;
