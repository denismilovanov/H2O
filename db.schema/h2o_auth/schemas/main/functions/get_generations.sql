----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_generations(
)
    RETURNS SETOF main.generations AS
$BODY$
DECLARE
BEGIN

   RETURN QUERY SELECT *
                    FROM main.generations
                    ORDER BY id ASC;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_generations(
) TO h2o_front;
