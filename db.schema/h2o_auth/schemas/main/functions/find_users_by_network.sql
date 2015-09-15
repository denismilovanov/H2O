----------------------------------------------------------------------------
-- поиск по социальному аккаунту

CREATE OR REPLACE FUNCTION main.find_users_by_network(
    i_network_id integer,
    ai_users_ids bigint[]
)
    RETURNS SETOF integer AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY SELECT user_id
                    FROM main.users_networks
                    WHERE   user_network_id = ANY(ai_users_ids) AND
                            network_id = i_network_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.find_users_by_network(
    i_network_id integer,
    ai_users_ids bigint[]
) TO h2o_front;
