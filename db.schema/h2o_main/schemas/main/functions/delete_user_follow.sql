----------------------------------------------------------------------------
-- удаление подписки

CREATE OR REPLACE FUNCTION main.delete_user_follow(
    i_user_id integer,
    i_follow_user_id integer
)
    RETURNS boolean AS
$BODY$
DECLARE

BEGIN

    DELETE FROM main.users_follows
        WHERE   user_id = i_user_id AND
                follow_user_id = i_follow_user_id;

    RETURN FOUND;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.delete_user_follow(
    i_user_id integer,
    i_follow_user_id integer
) TO h2o_front;
