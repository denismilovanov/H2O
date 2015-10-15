----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.send_invite_code(
    s_invite_code varchar
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.invite_codes
        SET status = 'awaiting_registration',
            invited_at = now()::timestamptz
        WHERE invite_code = s_invite_code;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.send_invite_code(
    s_invite_code varchar
) TO h2o_front;
