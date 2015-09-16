----------------------------------------------------------------------------
-- поиск по номеру в поколении

CREATE OR REPLACE FUNCTION main.get_user_id_by_num_in_generation(
    i_generation integer,
    i_num_in_generation integer
)
    RETURNS integer AS
$BODY$
DECLARE
    i_result_id integer;
BEGIN

    SELECT id INTO i_result_id
        FROM main.users
        WHERE   generation = i_generation AND
                num_in_generation = i_num_in_generation;

    RETURN i_result_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_id_by_num_in_generation(
    i_generation integer,
    i_num_in_generation integer
) TO h2o_front;
