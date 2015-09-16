----------------------------------------------------------------------------
-- список подписок

CREATE OR REPLACE FUNCTION notifications.get_all(
    i_user_id integer,
    i_limit integer,
    i_offset integer
)
    RETURNS SETOF notifications.all AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY SELECT *
                    FROM notifications.all
                    WHERE user_id = i_user_id
                    ORDER BY id DESC
                    LIMIT i_limit
                    OFFSET i_offset;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION notifications.get_all(
    i_user_id integer,
    i_limit integer,
    i_offset integer
) TO h2o_front;
