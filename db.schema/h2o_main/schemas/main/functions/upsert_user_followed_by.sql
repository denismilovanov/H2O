----------------------------------------------------------------------------
-- добавление подписчика

CREATE OR REPLACE FUNCTION main.upsert_user_followed_by(
    i_user_id integer,
    i_followed_by_user_id integer
)
    RETURNS boolean AS
$BODY$
DECLARE

BEGIN

    PERFORM 1
        FROM main.users_followed_by
        WHERE   user_id = i_user_id AND
                followed_by_user_id = i_followed_by_user_id;

    IF FOUND THEN
        RETURN FALSE;
    END IF;

    INSERT INTO main.users_followed_by
        (user_id, followed_by_user_id)
        SELECT i_user_id, i_followed_by_user_id;

    RETURN TRUE;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.upsert_user_followed_by(
    i_user_id integer,
    i_followed_by_user_id integer
) TO h2o_front;
