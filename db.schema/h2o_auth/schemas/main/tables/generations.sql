----------------------------------------------------------------------------
-- поколения

CREATE TABLE main.generations (
    id integer NOT NULL PRIMARY KEY,
    users_count integer NOT NULL,
    user_last_number integer NOT NULL
);


