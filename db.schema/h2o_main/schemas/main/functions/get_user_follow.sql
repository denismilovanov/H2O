----------------------------------------------------------------------------
-- поиск подписки по 2 участникам

CREATE OR REPLACE FUNCTION main.get_user_follow(
    i_user_id integer,
    i_follow_user_id integer
)
    RETURNS main.users_follows AS
$BODY$
DECLARE
    r_result main.users_follows;
BEGIN

    SELECT * INTO r_result
        FROM main.users_follows
        WHERE   user_id = i_user_id AND
                follow_user_id = i_follow_user_id;

    RETURN r_result;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_follow(
    i_user_id integer,
    i_follow_user_id integer
) TO h2o_front;
