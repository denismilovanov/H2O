----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_invite_codes_by_user_id(
    i_user_id integer
)
    RETURNS SETOF main.invite_codes AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY SELECT *
                    FROM main.invite_codes
                    WHERE owner_id = i_user_id
                    ORDER BY invite_code;
END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_invite_codes_by_user_id(
    i_user_id integer
) TO h2o_front;
