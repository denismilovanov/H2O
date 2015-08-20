----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_invite_code(
    s_invite_code varchar
)
    RETURNS main.invite_codes AS
$BODY$
DECLARE
    r_code main.invite_codes;
BEGIN

    SELECT * INTO r_code
        FROM main.invite_codes
        WHERE invite_code = s_invite_code;

    IF r_code.invite_code IS NULL THEN
        RETURN NULL;
    END IF;

    RETURN r_code;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_invite_code(
    s_invite_code varchar
) TO h2o_user;
