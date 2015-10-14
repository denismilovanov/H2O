----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.request_ios_build(
    s_invite_code varchar,
    i_user_id integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.invite_codes
        SET status = 'ios_build_requested'
        WHERE   invite_code = s_invite_code AND
                owner_id = i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.request_ios_build(
    s_invite_code varchar,
    i_user_id integer
) TO h2o_front;
