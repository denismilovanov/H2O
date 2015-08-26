----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_users_by_ids(
    ai_users_ids integer[]
)
    RETURNS SETOF main.users AS
$BODY$
DECLARE

BEGIN

   RETURN QUERY SELECT *
                    FROM main.users
                    WHERE id = ANY(ai_users_ids)
                    ORDER BY id ASC;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_users_by_ids(
    ai_users_ids integer[]
) TO h2o_front;

