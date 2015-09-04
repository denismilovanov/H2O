CREATE OR REPLACE FUNCTION public.get_test_name(
    i_sex integer
)
RETURNS varchar AS
$BODY$
DECLARE
    s_name varchar;
    s_surname varchar;
BEGIN

    IF i_sex = 1 THEN
        SELECT name INTO s_name
            FROM unnest(array[
                'Анастасия', 'Юлия', 'Мария', 'Анна', 'Екатерина', 'Виктория', 'Кристина', 'Ольга', 'Ирина', 'Елена',
                'Татьяна', 'Светлана', 'Настя', 'Ксения', 'Дарья', 'Александра', 'Алина', 'Наталья', 'Марина', 'Евгения',
                'Валерия', 'Катя', 'Даша', 'Аня', 'Полина', 'Яна', 'Юля', 'Диана', 'Карина', 'Алёна',
                'Елизавета', 'Маша', 'Маргарита', 'Наташа', 'Катерина', 'Оля'
            ]) AS name
            ORDER BY random()
            LIMIT 1;

        SELECT name INTO s_surname
            FROM unnest(array[
                'Константинова', 'Иванова', 'Петрова', 'Путина', 'Березовская', 'Медведева',
                'Константинопольская', 'Кудрина', 'Мединская', 'Навальная', 'Яшина', 'Собчак'
            ]) AS name
            ORDER BY random()
            LIMIT 1;

        RETURN s_name || ' ' || s_surname;

    END IF;

    IF i_sex = 2 THEN
        SELECT name INTO s_name
            FROM unnest(array[
                'Александр', 'Сергей', 'Дмитрий', 'Андрей', 'Алексей', 'Евгений', 'Максим', 'Денис', 'Антон', 'Роман',
                'Илья', 'Иван', 'Никита', 'Игорь', 'Дима', 'Павел', 'Олег', 'Владимир', 'Кирилл', 'Михаил', 'Николай',
                'Артём', 'Руслан', 'Виталий', 'Саша', 'Владислав', 'Вадим', 'Влад', 'Константин', 'Егор'
            ]) AS name
            ORDER BY random()
            LIMIT 1;

        SELECT name INTO s_surname
            FROM unnest(array[
                'Константинов', 'Иванов', 'Петров', 'Путин', 'Березовский', 'Медведев',
                'Константинопольский', 'Кудрин', 'Мединский', 'Навальный', 'Яшин', 'Собчак'
            ]) AS name
            ORDER BY random()
            LIMIT 1;

        RETURN s_name || ' ' || s_surname;
    END IF;



END
$BODY$
    LANGUAGE plpgsql VOLATILE;


