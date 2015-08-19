----------------------------------------------------------------------------
-- поиск uuid по токену

CREATE OR REPLACE FUNCTION main.get_user_uuid_by_access_token(
    s_access_token varchar
)
    RETURNS varchar AS
$BODY$
DECLARE
    s_user_uuid uuid;
BEGIN

    SELECT uuid INTO s_user_uuid
        FROM main.users
        WHERE id = (SELECT user_id FROM main.users_sessions WHERE access_token = s_access_token);

    RETURN s_user_uuid;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_uuid_by_access_token(
    s_access_token varchar
) TO h2o_user;
