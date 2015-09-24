----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_last_num_in_generation(
    i_generation integer
)
    RETURNS integer AS
$BODY$
DECLARE
    i_user_last_number integer;
BEGIN

    UPDATE main.generations
        SET user_last_number = user_last_number + 1,
            users_count = users_count + 1
        WHERE id = i_generation
        RETURNING user_last_number INTO i_user_last_number;

    RETURN i_user_last_number;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_last_num_in_generation(
    i_generation integer
) TO h2o_front;
