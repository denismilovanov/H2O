----------------------------------------------------------------------------
-- поиск по социальному аккаунту

CREATE OR REPLACE FUNCTION main.find_user_by_network(
    i_network_id integer,
    i_user_id bigint
)
    RETURNS integer AS
$BODY$
DECLARE
    i_user_id integer;
BEGIN

    SELECT user_id INTO i_user_id
        FROM main.users_networks
        WHERE   user_network_id = i_user_id AND
                network_id = i_network_id;

    RETURN i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.find_user_by_network(
    i_network_id integer,
    i_user_id bigint
) TO h2o_user;
