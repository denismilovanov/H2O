BEGIN;

alter table main.users_follows drop constraint users_follows_pkey;
alter table main.users_follows drop constraint users_follows_follow_user_id_fkey;
alter table main.users_follows drop constraint users_follows_user_id_fkey;

alter table main.users_follows rename to users_follows_old;

CREATE SEQUENCE main.users_follows_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE main.users_follows (
    id integer DEFAULT nextval('main.users_follows_id_seq') PRIMARY KEY,
    user_id integer REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    follow_user_id integer REFERENCES main.users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    followed_since timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT users_follows_ukey UNIQUE (user_id, follow_user_id)
);

ALTER TABLE main.users_follows
    ADD CONSTRAINT users_follows_not_equal
    CHECK (user_id != follow_user_id);

insert into main.users_follows
    (user_id, follow_user_id, followed_since)
    select user_id, follow_user_id, followed_since
        from main.users_follows_old;


drop table main.users_follows_old cascade;

CREATE OR REPLACE FUNCTION main.get_user_follow(
    i_user_id integer,
    i_follow_user_id integer
)
    RETURNS main.users_follows AS
$BODY$
DECLARE
    r_result main.users_follows;
BEGIN

    SELECT * INTO r_result
        FROM main.users_follows
        WHERE   user_id = i_user_id AND
                follow_user_id = i_follow_user_id;

    RETURN r_result;

END
$BODY$
    LANGUAGE plpgsql VOLATILE SECURITY DEFINER;


GRANT EXECUTE ON FUNCTION main.get_user_follow(
    i_user_id integer,
    i_follow_user_id integer
) TO h2o_front;


COMMIT;
