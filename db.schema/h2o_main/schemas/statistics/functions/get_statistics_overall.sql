----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION statistics.get_statistics_overall(
    i_user_id integer
)
    RETURNS statistics.overall AS
$BODY$
DECLARE
    r_result statistics.overall;
BEGIN

    SELECT * INTO r_result
        FROM statistics.overall
        WHERE user_id = i_user_id;

    r_result.supports_users_ids := subarray(r_result.supports_users_ids, 0, 5);
    r_result.receives_users_ids := subarray(r_result.receives_users_ids, 0, 5);

    RETURN r_result;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION statistics.get_statistics_overall(
    i_user_id integer
) TO h2o_front;
