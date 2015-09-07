----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.get_transactions_by_users_ids_and_dates(
    ai_users_ids integer[],
    d_from_date date,
    d_to_date date,
    t_direction billing.transaction_direction
)
    RETURNS SETOF billing.transactions AS
$BODY$
DECLARE

BEGIN

   RETURN QUERY SELECT *
                    FROM billing.transactions
                    WHERE   user_id = ANY(ai_users_ids) AND
                            date(created_at) BETWEEN d_from_date AND d_to_date AND
                            direction = t_direction
                    ORDER BY created_at DESC;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.get_transactions_by_users_ids_and_dates(
    ai_users_ids integer[],
    d_from_date date,
    d_to_date date,
    t_direction billing.transaction_direction
) TO h2o_front;

