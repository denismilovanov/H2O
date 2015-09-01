CREATE OR REPLACE FUNCTION public.format_datetime(
    ts_ts timestamp with time zone
)
RETURNS varchar AS
$BODY$
DECLARE
    s_datetime varchar;
BEGIN

    s_datetime := date_trunc('second', ts_ts at time zone 'UTC');

    s_datetime := replace(s_datetime, ' ', 'T');

    RETURN s_datetime;

END
$BODY$
    LANGUAGE plpgsql IMMUTABLE;


GRANT EXECUTE ON FUNCTION public.format_datetime(
    ts_ts timestamp with time zone
) TO PUBLIC;
