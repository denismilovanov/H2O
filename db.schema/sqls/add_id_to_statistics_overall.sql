BEGIN;

alter table statistics.overall drop constraint overall_pkey;
alter table statistics.overall drop constraint overall_user_id_fkey;

alter table statistics.overall rename to overall_old;

CREATE SEQUENCE statistics.overall_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE statistics.overall (
    id integer DEFAULT nextval('statistics.overall_id_seq') PRIMARY KEY,

    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    transaction_direction billing.transaction_direction NOT NULL,

    transactions_count integer NOT NULL DEFAULT 0,
    users_count integer NOT NULL DEFAULT 0,
    transactions_amount_sum numeric(15,2) NOT NULL DEFAULT 0.0,

    CONSTRAINT overall_ukey UNIQUE (user_id, transaction_direction)
);


insert into statistics.overall
    (user_id, transaction_direction, transactions_count, users_count, transactions_amount_sum)
    select user_id, transaction_direction, transactions_count, users_count, transactions_amount_sum
        from statistics.overall_old;


drop table statistics.overall_old cascade;

CREATE OR REPLACE FUNCTION statistics.get_statistics_overall(
    i_user_id integer
)
    RETURNS SETOF statistics.overall AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY SELECT *
                    FROM statistics.overall
                    WHERE user_id = i_user_id;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;

GRANT EXECUTE ON FUNCTION statistics.get_statistics_overall(
    i_user_id integer
) TO h2o_front;


CREATE OR REPLACE FUNCTION statistics.create_user_records(
    i_user_id integer
)
    RETURNS void AS
$BODY$
DECLARE

BEGIN

    INSERT INTO statistics.overall
        (user_id, transaction_direction)
        SELECT  i_user_id, unnest(array['support', 'receive']::billing.transaction_direction[]);

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION statistics.create_user_records(
    i_user_id integer
) TO h2o_front;

COMMIT;
