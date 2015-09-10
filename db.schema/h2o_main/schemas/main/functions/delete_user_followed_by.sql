---------------------------------------------------------------------------
-- удаление подписчика

CREATE OR REPLACE FUNCTION main.delete_user_followed_by(
    i_user_id integer,
    i_followed_by_user_id integer
)
    RETURNS boolean AS
$BODY$
DECLARE

BEGIN

    DELETE FROM main.users_followed_by
        WHERE   user_id = i_user_id AND
                followed_by_user_id = i_followed_by_user_id;

    RETURN FOUND;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.delete_user_followed_by(
    i_user_id integer,
    i_followed_by_user_id integer
) TO h2o_front;
