----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION main.drop_push_tokens(
    i_ios_seconds integer DEFAULT 86400 * 7,
    i_android_seconds integer DEFAULT 86400 * 7
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    DELETE FROM main.users_devices
        WHERE   updated_at < now() - interval '1 second' * i_ios_seconds AND
                device_type = 'ios';

    DELETE FROM main.users_devices
        WHERE   updated_at < now() - interval '1 second' * i_android_seconds AND
                device_type = 'android';

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.drop_push_tokens(
    i_ios_seconds integer,
    i_android_seconds integer
) TO h2o_front;
