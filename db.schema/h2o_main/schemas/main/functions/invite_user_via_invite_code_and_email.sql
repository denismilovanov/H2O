----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.invite_user_via_invite_code_and_email(
    s_invite_code varchar,
    s_email varchar
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.invite_codes
        SET email = s_email,
            status = 'sending'
        WHERE invite_code = s_invite_code;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.invite_user_via_invite_code_and_email(
    s_invite_code varchar,
    s_email varchar
) TO h2o_front;
