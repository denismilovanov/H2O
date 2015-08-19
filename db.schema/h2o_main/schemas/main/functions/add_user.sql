----------------------------------------------------------------------------
-- добавление пользователя

CREATE OR REPLACE FUNCTION main.add_user(
    s_first_name varchar,
    s_last_name varchar
)
    RETURNS uuid AS
$BODY$
DECLARE
    r_user record;
BEGIN

    INSERT INTO main.users
        (first_name, last_name, invite_code)
        SELECT s_first_name, s_last_name, ''
        RETURNING uuid, id INTO r_user;

    INSERT INTO main.users_sessions
        SELECT r_user.id;

    RETURN r_user.uuid;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.add_user(
    s_first_name varchar,
    s_last_name varchar
) TO h2o_user;
