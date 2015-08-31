----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION statistics.get_statistics_counter_users(
    i_user_id integer,
    t_transaction_direction main.transaction_direction,
    i_limit integer,
    i_offset integer
)
    RETURNS SETOF statistics.counter_users AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY SELECT *
                    FROM statistics.counter_users
                    WHERE   user_id = i_user_id AND
                            transaction_direction = t_transaction_direction
                    ORDER BY counter_user_id ASC
                    LIMIT i_limit
                    OFFSET i_offset;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION statistics.get_statistics_counter_users(
    i_user_id integer,
    t_transaction_direction main.transaction_direction,
    i_limit integer,
    i_offset integer
) TO h2o_front;
