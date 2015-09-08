----------------------------------------------------------------------------
-- восстановление профиля

CREATE OR REPLACE FUNCTION main.undelete_user_profile(
    i_user_id integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.users
        SET is_deleted = 'f'
        WHERE id = i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.undelete_user_profile(
    i_user_id integer
) TO h2o_front;
