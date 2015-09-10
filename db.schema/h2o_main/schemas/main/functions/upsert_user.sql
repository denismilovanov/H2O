----------------------------------------------------------------------------
-- добавление или обновление пользователя

CREATE OR REPLACE FUNCTION main.upsert_user(
    i_user_id integer,
    s_name varchar,
    s_avatar_url varchar,
    u_user_uuid uuid DEFAULT NULL,
    i_network_id integer DEFAULT NULL,
    i_user_network_id bigint DEFAULT NULL,
    i_generation integer DEFAULT NULL,
    i_num_in_generation integer DEFAULT NULL
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
        (id, name, avatar_url, uuid, facebook_id, generation, num_in_generation)
        SELECT  i_user_id,
                s_name,
                s_avatar_url,
                u_user_uuid,
                i_user_network_id,
                i_generation,
                i_num_in_generation
        RETURNING uuid INTO u_uuid;

    RETURN u_uuid;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.upsert_user(
    i_user_id integer,
    s_name varchar,
    s_avatar_url varchar,
    u_user_uuid uuid,
    i_network_id integer,
    i_user_network_id bigint,
    i_generation integer,
    i_num_in_generation integer
) TO h2o_front;
