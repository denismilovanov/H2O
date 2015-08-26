----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_users(
    i_limit integer,
    i_offset integer
)
    RETURNS SETOF main.users AS
$BODY$
DECLARE
    r_user main.users;
BEGIN

   RETURN QUERY SELECT *
                    FROM main.users
                    ORDER BY id ASC
                    LIMIT i_limit
                    OFFSET i_offset;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION  main.get_users(
    i_limit integer,
    i_offset integer
) TO h2o_front;

