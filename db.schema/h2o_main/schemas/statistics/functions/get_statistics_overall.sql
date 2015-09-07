----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION statistics.get_statistics_overall(
    i_user_id integer
)
    RETURNS SETOF statistics.overall AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY SELECT *
                    FROM statistics.overall
                    WHERE user_id = i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION statistics.get_statistics_overall(
    i_user_id integer
) TO h2o_front;
