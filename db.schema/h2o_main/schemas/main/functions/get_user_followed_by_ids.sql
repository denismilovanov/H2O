----------------------------------------------------------------------------
-- список подписчиков

CREATE OR REPLACE FUNCTION main.get_user_followed_by_ids(
    i_user_id integer,
    i_limit_id integer,
    i_offset_id integer
)
    RETURNS SETOF integer AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY SELECT followed_by_user_id
                    FROM main.users_followed_by
                    WHERE user_id = i_user_id
                    ORDER BY followed_by_user_id ASC
                    LIMIT i_limit_id
                    OFFSET i_offset_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_followed_by_ids(
    i_user_id integer,
    i_limit_id integer,
    i_offset_id integer
) TO h2o_front;
