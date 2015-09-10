----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_users_ids_by_generation(
    i_generation_id integer
)
    RETURNS SETOF integer AS
$BODY$
DECLARE
BEGIN

   RETURN QUERY SELECT user_id
                    FROM main.generations_users
                    WHERE generation_id = i_generation_id
                    ORDER BY user_id ASC;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_users_ids_by_generation(
    i_generation_id integer
) TO h2o_front;
