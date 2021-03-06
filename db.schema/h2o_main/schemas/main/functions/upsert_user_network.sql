----------------------------------------------------------------------------
-- добавление или обновление социального аккаунта

CREATE OR REPLACE FUNCTION main.upsert_user_network(
    i_user_id integer,
    i_network_id integer,
    i_user_network_id bigint,
    s_access_token varchar
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.users_networks
        SET access_token = s_access_token
        WHERE   user_network_id = i_user_network_id AND
                network_id = i_network_id;

    IF NOT FOUND THEN
        INSERT INTO main.users_networks
            (user_id, network_id, user_network_id, access_token)
            VALUES (
                i_user_id,
                i_network_id,
                i_user_network_id,
                s_access_token
            );
    END IF;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.upsert_user_network(
    i_user_id integer,
    i_network_id integer,
    i_user_id bigint,
    s_access_token varchar
) TO h2o_front;
