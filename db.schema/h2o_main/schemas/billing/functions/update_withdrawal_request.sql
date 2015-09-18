----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.update_withdrawal_request(
    i_user_id integer,
    i_withdrawal_request_id bigint,
    t_status billing.withdrawal_request_status,
    j_request_data jsonb,
    j_response_data jsonb,
    i_our_transaction_id bigint
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE billing.withdrawal_requests
        SET status = t_status,
            billed_at = CASE WHEN t_status = 'success' THEN now() ELSE NULL END,
            request_data = j_request_data,
            response_data = j_response_data,
            our_transaction_id = i_our_transaction_id
        WHERE   id = i_withdrawal_request_id AND
                user_id = i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.update_withdrawal_request(
    i_user_id integer,
    i_withdrawal_request_id bigint,
    t_status billing.withdrawal_request_status,
    j_request_data jsonb,
    j_response_data jsonb,
    i_our_transaction_id bigint
) TO h2o_front;

