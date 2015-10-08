----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_users_ids_by_generation(
    i_generation_id integer,
    b_debug boolean DEFAULT FALSE
)
    RETURNS SETOF integer AS
$BODY$
DECLARE
BEGIN

   RETURN QUERY SELECT id
                    FROM main.users
                    WHERE   generation = i_generation_id AND
                            CASE WHEN b_debug
                                THEN TRUE
                                ELSE id >= 0 -- skip test users in production
                            END
                    ORDER BY id ASC;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_users_ids_by_generation(
    i_generation_id integer,
    b_debug boolean
) TO h2o_front;
