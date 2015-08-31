----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION statistics.get_statistics_overall(
    i_user_id integer
)
    RETURNS SETOF statistics.overall AS
$BODY$
DECLARE
    r_result statistics.overall;
BEGIN

    FOR r_result IN SELECT *
                        FROM statistics.overall
                        WHERE user_id = i_user_id
    LOOP

        r_result.users_ids := subarray(r_result.users_ids, 0, 5);

        RETURN NEXT r_result;

    END LOOP;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION statistics.get_statistics_overall(
    i_user_id integer
) TO h2o_front;
