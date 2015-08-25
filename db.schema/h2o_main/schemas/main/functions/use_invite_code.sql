----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.use_invite_code(
    s_invite_code varchar,
    i_user_id integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.invite_codes
        SET is_used = 't',
            invited_user_id = i_user_id,
            used_at = now(),
            status = 'used'
        WHERE invite_code = s_invite_code;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.use_invite_code(
    s_invite_code varchar,
    i_user_id integer
) TO h2o_user;
