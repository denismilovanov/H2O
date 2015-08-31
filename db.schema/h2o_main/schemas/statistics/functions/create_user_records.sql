----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION statistics.create_user_records(
    i_user_id integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    INSERT INTO statistics.overall
        SELECT  i_user_id, unnest(array['support', 'receive']::main.transaction_direction[]);

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION statistics.create_user_records(
    i_user_id integer
) TO h2o_front;
