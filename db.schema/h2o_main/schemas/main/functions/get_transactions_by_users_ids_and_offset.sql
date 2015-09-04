----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_transactions_by_users_ids_and_offset(
    ai_users_ids integer[],
    i_limit integer,
    i_offset integer
)
    RETURNS SETOF main.transactions AS
$BODY$
DECLARE

BEGIN

   RETURN QUERY SELECT *
                    FROM main.transactions
                    WHERE user_id = ANY(ai_users_ids)
                    ORDER BY created_at DESC
                    LIMIT i_limit
                    OFFSET i_offset;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_transactions_by_users_ids_and_offset(
    ai_users_ids integer[],
    i_limit integer,
    i_offset integer
) TO h2o_front;

