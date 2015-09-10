INSERT INTO main.generations
    SELECT i, 0, 0
        FROM generate_series(1, 100) AS i;


