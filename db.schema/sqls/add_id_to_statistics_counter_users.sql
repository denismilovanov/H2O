BEGIN;

alter table statistics.counter_users drop constraint counter_users_pkey;
alter table statistics.counter_users drop constraint counter_users_user_id_fkey;

alter table statistics.counter_users rename to counter_users_old;

CREATE SEQUENCE statistics.counter_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE statistics.counter_users (
    id integer DEFAULT nextval('statistics.counter_users_id_seq') PRIMARY KEY,

    user_id integer NOT NULL REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    counter_user_id integer NOT NULL, -- 0 для анонимных поступлений
    transaction_direction billing.transaction_direction NOT NULL,

    transactions_count integer NOT NULL DEFAULT 0,
    transactions_amount_sum numeric(15,2) NOT NULL DEFAULT 0,

    CONSTRAINT counter_users_ukey UNIQUE (user_id, counter_user_id, transaction_direction)
);

insert into statistics.counter_users
    (user_id, counter_user_id, transaction_direction, transactions_count, transactions_amount_sum)
    select user_id, counter_user_id, transaction_direction, transactions_count, transactions_amount_sum
        from statistics.counter_users_old;


drop table statistics.counter_users_old cascade;

----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION statistics.get_statistics_counter_users(
    i_user_id integer,
    t_transaction_direction billing.transaction_direction,
    i_limit integer,
    i_offset integer
)
    RETURNS SETOF statistics.counter_users AS
$BODY$
DECLARE

BEGIN

    RETURN QUERY SELECT *
                    FROM statistics.counter_users
                    WHERE   user_id = i_user_id AND
                            transaction_direction = t_transaction_direction
                    ORDER BY transactions_amount_sum DESC, counter_user_id ASC
                    LIMIT i_limit
                    OFFSET i_offset;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION statistics.get_statistics_counter_users(
    i_user_id integer,
    t_transaction_direction billing.transaction_direction,
    i_limit integer,
    i_offset integer
) TO h2o_front;


COMMIT;
