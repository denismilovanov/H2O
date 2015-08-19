----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.use_invite_code(
    s_invite_code varchar,
    u_user_uuid uuid
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.invite_codes
        SET is_used = 't',
            invited_user_id = (SELECT id FROM main.get_user_by_uuid(u_user_uuid))
        WHERE code = s_invite_code;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.use_invite_code(
    s_invite_code varchar,
    u_user_uuid uuid
) TO h2o_user;
