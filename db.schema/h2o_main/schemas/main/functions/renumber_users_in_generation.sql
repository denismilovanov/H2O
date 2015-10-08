----------------------------------------------------------------------------
-- перенумерация всех пользователей поколения
-- очень тяжелая операция, обращаться с осторожностью!

CREATE OR REPLACE FUNCTION main.renumber_users_in_generation(
    i_generation_id integer,
    b_debug boolean DEFAULT FALSE
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
                    WHERE   generation = i_generation_id AND
                            CASE WHEN b_debug
                                THEN TRUE
                                ELSE id >= 0 -- skip test users in production
                            END
                    ORDER BY id ASC
    LOOP

        UPDATE main.users
            SET num_in_generation = i_count
            WHERE id = r_user.id;

        RAISE NOTICE '%: % -> %', i_generation_id, r_user.id, i_count;

        i_count := i_count + 1;

    END LOOP;


    UPDATE main.generations
        SET users_count = i_count,
            user_last_number = i_count - 1
        WHERE id = i_generation_id;


    CREATE UNIQUE INDEX users_generations_ukey
        ON main.users
        USING btree(generation, num_in_generation);

    RETURN i_count - 1;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.renumber_users_in_generation(
    i_generation_id integer,
    b_debug boolean
) TO h2o_owner;


