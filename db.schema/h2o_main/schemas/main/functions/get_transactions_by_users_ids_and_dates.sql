----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_transactions_by_users_ids_and_dates(
    ai_users_ids integer[],
    d_from_date date,
    d_to_date date,
    t_direction main.transaction_direction
)
    RETURNS SETOF main.transactions AS
$BODY$
DECLARE

BEGIN

   RETURN QUERY SELECT *
                    FROM main.transactions
                    WHERE   user_id = ANY(ai_users_ids) AND
                            date(created_at) BETWEEN d_from_date AND d_to_date AND
                            direction = t_direction
                    ORDER BY created_at DESC;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_transactions_by_users_ids_and_dates(
    ai_users_ids integer[],
    d_from_date date,
    d_to_date date,
    t_direction main.transaction_direction
) TO h2o_front;

