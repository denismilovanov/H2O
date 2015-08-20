----------------------------------------------------------------------------
-- обновление профиля

CREATE OR REPLACE FUNCTION main.update_user_profile(
    i_user_id integer,
    t_visibility main.user_visibility,
    t_status main.user_status
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.users
        SET status = COALESCE(t_status, status),
            visibility = COALESCE(t_visibility, visibility)
        WHERE id = i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.update_user_profile(
    i_user_id integer,
    t_visibility main.user_visibility,
    t_status main.user_status
) TO h2o_user;
