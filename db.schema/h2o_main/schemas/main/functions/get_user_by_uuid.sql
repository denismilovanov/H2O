----------------------------------------------------------------------------
-- поиск по uuid

CREATE OR REPLACE FUNCTION main.get_user_by_uuid(
    s_uuid uuid
)
    RETURNS main.users AS
$BODY$
DECLARE
    r_user main.users;
BEGIN

    SELECT * INTO r_user
        FROM main.users
        WHERE uuid = s_uuid;

    IF r_user.id IS NULL THEN
        RETURN NULL;
    END IF;

    RETURN r_user;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_by_uuid(
    s_uuid uuid
) TO h2o_user;
