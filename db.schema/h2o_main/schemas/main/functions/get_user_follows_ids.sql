----------------------------------------------------------------------------
-- список подписок

CREATE OR REPLACE FUNCTION main.get_user_follows_ids(
    i_user_id integer,
    i_limit_id integer,
    i_offset_id integer
)
    RETURNS SETOF integer AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY SELECT follow_user_id
                    FROM main.users_follows
                    WHERE user_id = i_user_id
                    ORDER BY follow_user_id ASC
                    LIMIT i_limit_id
                    OFFSET i_offset_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_follows_ids(
    i_user_id integer,
    i_limit_id integer,
    i_offset_id integer
) TO h2o_user;
