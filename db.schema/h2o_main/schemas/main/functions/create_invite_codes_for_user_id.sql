----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.create_invite_codes_for_user_id(
    i_user_id integer,
    i_count integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    INSERT INTO main.invite_codes
        (invite_code, owner_id)
        SELECT  upper(encode(gen_random_bytes(6), 'hex')),
                i_user_id
            FROM generate_series(1, i_count);


END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.create_invite_codes_for_user_id(
    i_user_id integer,
    i_count integer
) TO h2o_front;
