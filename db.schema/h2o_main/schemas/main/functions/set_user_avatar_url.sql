----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.set_user_avatar_url(
    i_user_id integer,
    s_avatar_url varchar
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    UPDATE main.users
        SET avatar_url = s_avatar_url
        WHERE id = i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.set_user_avatar_url(
    i_user_id integer,
    s_avatar_url varchar
) TO h2o_front;
