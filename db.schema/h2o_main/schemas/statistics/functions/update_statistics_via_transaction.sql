----------------------------------------------------------------------------
--

CREATE OR REPLACE FUNCTION statistics.update_statistics_via_transaction(
    i_user_id integer,
    i_counter_user_id integer,
    t_direction billing.transaction_direction,
    n_amount numeric,
    t_currency main.currency,
    b_is_anonymous boolean
)
    RETURNS void AS
$BODY$
DECLARE
    i_users_count integer;
BEGIN

    IF t_direction = 'receive' AND b_is_anonymous THEN
        i_counter_user_id := 0;
    END IF;

    UPDATE statistics.counter_users
        SET transactions_count = transactions_count + 1,
            amount_sum = amount_sum + n_amount
        WHERE   user_id = i_user_id AND
                counter_user_id IS NOT DISTINCT FROM i_counter_user_id AND
                transaction_direction = t_direction;

    IF NOT FOUND THEN
        INSERT INTO statistics.counter_users
            (user_id, counter_user_id, transaction_direction, transactions_count, amount_sum)
            VALUES (
                i_user_id,
                i_counter_user_id,
                t_direction,
                1,
                n_amount
            );
    END IF;

    SELECT count(DISTINCT counter_user_id) INTO i_users_count
        FROM statistics.counter_users
        WHERE   user_id = i_user_id AND
                transaction_direction = t_direction AND
                counter_user_id IS NOT NULL;

    i_users_count := COALESCE(i_users_count, 0);

    UPDATE statistics.overall
        SET transactions_count = transactions_count + 1,
            users_count = i_users_count
        WHERE   user_id = i_user_id AND
                transaction_direction = t_direction;

    IF NOT FOUND THEN
        INSERT INTO statistics.overall
            (user_id, transaction_direction, transactions_count, users_count)
            VALUES (
                i_user_id,
                t_direction,
                1,
                i_users_count
            );
    END IF;


END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION statistics.update_statistics_via_transaction(
    i_user_id integer,
    i_counter_user_id integer,
    t_direction billing.transaction_direction,
    n_amount numeric,
    t_currency main.currency,
    b_is_anonymous boolean
) TO h2o_front;

