----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.get_withdrawal_request_by_id(
    i_user_id integer,
    i_withdrawal_request_id bigint
)
    RETURNS billing.withdrawal_requests AS
$BODY$
DECLARE
    r_record billing.withdrawal_requests;
BEGIN

    SELECT * INTO r_record
        FROM billing.withdrawal_requests
        WHERE   id = i_withdrawal_request_id AND
                user_id = i_user_id;

    RETURN r_record;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.get_withdrawal_request_by_id(
    i_user_id integer,
    i_withdrawal_request_id bigint
) TO h2o_front;

