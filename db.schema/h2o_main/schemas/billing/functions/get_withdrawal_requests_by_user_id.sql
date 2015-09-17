----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.get_withdrawal_requests_by_user_id(
    i_user_id integer,
    i_limit integer,
    i_offset integer
)
    RETURNS SETOF billing.withdrawal_requests AS
$BODY$
DECLARE

BEGIN

   RETURN QUERY SELECT *
                    FROM billing.withdrawal_requests
                    WHERE user_id = i_user_id
                    ORDER BY created_at DESC, id DESC
                    LIMIT i_limit
                    OFFSET i_offset;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.get_withdrawal_requests_by_user_id(
    i_user_id integer,
    i_limit integer,
    i_offset integer
) TO h2o_front;

