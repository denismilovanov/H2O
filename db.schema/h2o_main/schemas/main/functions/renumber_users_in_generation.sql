----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.renumber_users_in_generation(
    i_generation_id integer
)
    RETURNS integer AS
$BODY$
DECLARE
    r_user record;
    i_count integer := 0;
BEGIN

    DROP INDEX main.users_generations_ukey;

    FOR r_user IN SELECT *
                    FROM main.users
                    WHERE generation = i_generation_id
                    ORDER BY id ASC
    LOOP

        UPDATE main.users
            SET num_in_generation = i_count
            WHERE id = r_user.id;

        RAISE NOTICE '%: % -> %', i_generation_id, r_user.id, i_count;

        i_count := i_count + 1;

    END LOOP;


    CREATE UNIQUE INDEX users_generations_ukey
        ON main.users
        USING btree(generation, num_in_generation);

    RETURN i_count - 1;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.renumber_users_in_generation(
    i_generation_id integer
) TO PUBLIC;


