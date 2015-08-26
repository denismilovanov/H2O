INSERT INTO main.users_networks
    (user_id, user_network_id, network_id)
    VALUES
    (- 1, - 1, 1),
    (- 2, - 2, 1),
    (- 3, - 3, 1),
    (- 4, - 4, 1),
    (- 5, - 5, 1),
    (- 6, - 6, 1),
    (- 7, - 7, 1),
    (- 8, - 8, 1),
    (- 9, - 9, 1),
    (-10, -10, 1);

-- for real users
ALTER SEQUENCE main.users_id_seq RESTART WITH 100000;
