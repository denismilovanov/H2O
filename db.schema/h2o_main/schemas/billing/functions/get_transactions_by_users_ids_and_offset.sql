----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.get_transactions_by_users_ids_and_offset(
    ai_users_ids integer[],
    i_limit integer,
    i_offset integer,
    ai_exclude_counter_users_ids integer[] DEFAULT NULL
)
    RETURNS SETOF billing.transactions AS
$BODY$
DECLARE

BEGIN

    ai_exclude_counter_users_ids := coalesce(ai_exclude_counter_users_ids, array[]::integer[]);

    RETURN QUERY SELECT *
                    FROM billing.transactions
                    WHERE   user_id = ANY(ai_users_ids) AND
                            counter_user_id IS NOT NULL AND
                            NOT counter_user_id = ANY(ai_exclude_counter_users_ids)
                    ORDER BY created_at DESC, id DESC
                    LIMIT i_limit
                    OFFSET i_offset;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.get_transactions_by_users_ids_and_offset(
    ai_users_ids integer[],
    i_limit integer,
    i_offset integer,
    ai_exclude_counter_users_ids integer[]
) TO h2o_front;

