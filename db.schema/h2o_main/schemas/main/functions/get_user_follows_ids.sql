----------------------------------------------------------------------------
-- список подписок

CREATE OR REPLACE FUNCTION main.get_user_follows_ids(
    i_user_id integer,
    i_limit_id integer,
    i_offset_id integer,
    s_search_query varchar
)
    RETURNS SETOF integer AS
$BODY$
DECLARE

BEGIN

    IF s_search_query IS NULL THEN

        RETURN QUERY SELECT follow_user_id
                        FROM main.users_follows
                        WHERE user_id = i_user_id
                        ORDER BY follow_user_id ASC
                        LIMIT i_limit_id
                        OFFSET i_offset_id;

    ELSE

        RETURN QUERY SELECT uf.follow_user_id
                        FROM main.users_follows AS uf

                        -- hard to scale: possible join to other db
                        INNER JOIN main.users AS u
                            ON  uf.follow_user_id = u.id AND
                                public.normalize(u.name) ~* public.normalize(s_search_query)

                        WHERE uf.user_id = i_user_id
                        ORDER BY uf.follow_user_id ASC
                        LIMIT i_limit_id
                        OFFSET i_offset_id;

    END IF;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_follows_ids(
    i_user_id integer,
    i_limit_id integer,
    i_offset_id integer,
    s_search_query varchar
) TO h2o_front;
