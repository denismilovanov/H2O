----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_user_free_invites_count(
    i_user_id integer
)
    RETURNS integer AS
$BODY$
DECLARE
    i_count integer;
BEGIN

    SELECT count(1) INTO i_count
        FROM main.invite_codes
        WHERE   owner_id = i_user_id AND
                status = 'free';

    RETURN i_count;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_free_invites_count(
    i_user_id integer
) TO h2o_front;
