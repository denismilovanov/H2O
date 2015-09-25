----------------------------------------------------------------------------
-- число follows

CREATE OR REPLACE FUNCTION main.get_user_follows_count(
    i_user_id integer
)
    RETURNS integer AS
$BODY$
DECLARE
    i_count integer;
BEGIN

    SELECT count(*) INTO i_count
        FROM main.users_follows
        WHERE user_id = i_user_id;

    RETURN i_count;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_follows_count(
    i_user_id integer
) TO h2o_front;
