----------------------------------------------------------------------------
-- добавление пользователя

CREATE OR REPLACE FUNCTION main.add_user(
    s_name varchar,
    s_avatar_url varchar
)
    RETURNS uuid AS
$BODY$
DECLARE
    r_user record;
BEGIN

    INSERT INTO main.users
        (name, avatar_url)
        SELECT s_name, s_avatar_url
        RETURNING uuid, id INTO r_user;

    INSERT INTO main.users_sessions
        SELECT r_user.id;

    RETURN r_user.uuid;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.add_user(
    s_name varchar,
    s_avatar_url varchar
) TO h2o_user;
