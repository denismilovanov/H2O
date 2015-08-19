----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_user_networks(
    i_user_id integer
)
    RETURNS SETOF main.users_networks AS
$BODY$
DECLARE
    r_user_network main.users_networks;
BEGIN

   RETURN QUERY SELECT *
                    FROM main.users_networks
                    WHERE user_id = i_user_id
                    ORDER BY network_id ASC;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_networks(
    i_user_id integer
) TO h2o_user;
