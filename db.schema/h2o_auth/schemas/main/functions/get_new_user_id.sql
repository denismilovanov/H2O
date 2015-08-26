----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.get_new_user_id(
)
    RETURNS record AS
$BODY$
DECLARE
    r_record record;
    i_user_id integer;
    s_uuid varchar;
BEGIN

    i_user_id := nextval('main.users_id_seq');
    s_uuid := uuid_generate_v4()::varchar;
    s_uuid := substring(s_uuid from 10);

    s_uuid := lpad(to_hex(i_user_id), 8, '0') || '-' || s_uuid;

    RAISE NOTICE '%', s_uuid;

    SELECT  i_user_id AS user_id,
            s_uuid::uuid AS user_uuid
        INTO r_record;

    RETURN r_record;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_new_user_id(
) TO h2o_front;
