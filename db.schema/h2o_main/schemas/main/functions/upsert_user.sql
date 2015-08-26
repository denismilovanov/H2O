----------------------------------------------------------------------------
-- добавление или обновление пользователя

CREATE OR REPLACE FUNCTION main.upsert_user(
    i_user_id integer,
    s_name varchar,
    s_avatar_url varchar,
    u_user_uuid uuid DEFAULT NULL
)
    RETURNS uuid AS
$BODY$
DECLARE
    u_uuid uuid;
BEGIN

    UPDATE main.users
        SET name = s_name,
            avatar_url = s_avatar_url
        WHERE id = i_user_id
        RETURNING uuid INTO u_uuid;

    IF FOUND THEN
        RETURN u_uuid;
    END IF;

    INSERT INTO main.users
        (id, name, avatar_url, uuid)
        SELECT  i_user_id,
                s_name,
                s_avatar_url,
                u_user_uuid
        RETURNING uuid INTO u_uuid;

    RETURN u_uuid;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.upsert_user(
    i_user_id integer,
    s_name varchar,
    s_avatar_url varchar,
    u_user_uuid uuid
) TO h2o_front;
