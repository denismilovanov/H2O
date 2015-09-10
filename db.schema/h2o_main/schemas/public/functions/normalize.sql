----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION public.normalize(
    s_string varchar
)
    RETURNS varchar AS
$BODY$
DECLARE

BEGIN

    RETURN lower(regexp_replace(s_string, '[^A-ZА-Яa-zа-я\d]', '', 'g'));

END
$BODY$
    LANGUAGE plpgsql STABLE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION public.normalize(
    s_string varchar
) TO h2o_front;
