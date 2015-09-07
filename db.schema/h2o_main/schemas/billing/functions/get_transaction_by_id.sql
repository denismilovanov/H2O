----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION billing.get_transaction_by_id(
    i_user_id integer,
    i_transaction_id bigint
)
    RETURNS billing.transactions AS
$BODY$
DECLARE
    r_record billing.transactions;
BEGIN

    SELECT * INTO r_record
        FROM billing.transactions
        WHERE   id = i_transaction_id AND
                user_id = i_user_id;

    RETURN r_record;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION billing.get_transaction_by_id(
    i_user_id integer,
    i_transaction_id bigint
) TO h2o_front;

