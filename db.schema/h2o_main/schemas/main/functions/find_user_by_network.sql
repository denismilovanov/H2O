----------------------------------------------------------------------------
-- поиск по социальному аккаунту

CREATE OR REPLACE FUNCTION main.find_user_by_network(
    i_network_id integer,
    i_user_id bigint
)
    RETURNS uuid AS
$BODY$
DECLARE
    s_uuid uuid;
BEGIN

    SELECT uuid INTO s_uuid
        FROM main.users
        WHERE id = (
            SELECT user_id
                FROM main.users_networks
                WHERE   user_network_id = i_user_id AND
                        network_id = i_network_id
        );

    RETURN s_uuid;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.find_user_by_network(
    i_network_id integer,
    i_user_id bigint
) TO h2o_user;
