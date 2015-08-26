----------------------------------------------------------------------------
-- добавление подписки

CREATE OR REPLACE FUNCTION main.upsert_user_follow(
    i_user_id integer,
    i_follow_user_id integer
)
    RETURNS boolean AS
$BODY$
DECLARE

BEGIN

    PERFORM 1
        FROM main.users_follows
        WHERE   user_id = i_user_id AND
                follow_user_id = i_follow_user_id;

    IF FOUND THEN
        RETURN FALSE;
    END IF;

    INSERT INTO main.users_follows
        (user_id, follow_user_id)
        SELECT i_user_id, i_follow_user_id;

    RETURN TRUE;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.upsert_user_follow(
    i_user_id integer,
    i_follow_user_id integer
) TO h2o_front;
