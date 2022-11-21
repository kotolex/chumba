from unittest import TestCase, main

from src.word import Word

DATA = ['ёкать', 'ёмкий', 'ёрник', 'аббат', 'абзац', 'аборт', 'абрек', 'абрис', 'авизо', 'аврал', 'автол', 'агент',
        'агнец', 'адепт', 'адрес']


class TestWord(TestCase):
    def test_simple_object(self):
        word = Word(10)
        self.assertEqual(word.cached, [])
        self.assertEqual(word.length, 10)
        self.assertEqual(word.dictionary, Word.RU)

    def test_en_dict(self):
        word = Word(10, False)
        self.assertEqual(word.cached, [])
        self.assertEqual(word.length, 10)
        self.assertEqual(word.dictionary, Word.EN)

    def test_limit(self):
        params = (
            (DATA, -1),
            (DATA, 0),
            (['ёкать'], 1),
            (['ёкать', 'ёмкий', 'ёрник'], 3),
            (DATA, 15),
            (DATA, 100),
        )
        for expected, limit in params:
            with self.subTest(f'Test limit {limit}'):
                word = Word(5)
                word.cached = DATA
                result = word.examples(limit)
                self.assertEqual(expected, result)

    def test_starts_with_raises_when_bigger_than_length(self):
        word = Word(1)
        with self.assertRaises(ValueError) as e:
            word.starts_with('22')
        self.assertEqual(str(e.exception), "Prefix 22 is bigger than word length(1)")

    def test_starts_with_do_nothing_when_empty(self):
        word = Word(1)
        cond = word.conditions[:]
        word.starts_with('')
        self.assertEqual(cond, word.conditions)

    def test_starts_with_appends_to_conditions(self):
        word = Word(12)
        cond = word.conditions[:]
        word.starts_with('12')
        self.assertEqual(len(cond) + 1, len(word.conditions))

    def test_ends_with_raises_when_bigger_than_length(self):
        word = Word(1)
        with self.assertRaises(ValueError) as e:
            word.ends_with('22')
        self.assertEqual(str(e.exception), "Postfix 22 is bigger than word length(1)")

    def test_ends_with_do_nothing_when_empty(self):
        word = Word(1)
        cond = word.conditions[:]
        word.ends_with('')
        self.assertEqual(cond, word.conditions)

    def test_ends_with_appends_to_conditions(self):
        word = Word(12)
        cond = word.conditions[:]
        word.ends_with('12')
        self.assertEqual(len(cond) + 1, len(word.conditions))

    def test_starts_with_works(self):
        params = (
            (['агент', 'агнец'], 'АГ'),
            (['агент', 'агнец'], 'аг'),
            ([], 'W'),
            (['ёмкий'], 'ёмкий'),
            (['ёмкий'], 'ёмки'),
            (['ёмкий'], 'ёмк'),
            (['ёмкий'], 'ём'),
            (['ёкать', 'ёмкий', 'ёрник'], 'ё'),
        )
        for expected, prefix in params:
            with self.subTest(f'Test starts with {prefix}'):
                word = Word(5)
                word.cached = DATA
                word.starts_with(prefix)
                result = word.examples(5)
                self.assertEqual(expected, result)

    def test_ends_with_works(self):
        params = (
            (['аврал', 'автол'], 'л'),
            (['аврал', 'автол'], 'Л'),
            (['агнец'], 'агнец'),
            (['агнец'], 'гнец'),
            (['агнец'], 'нец'),
            (['агнец'], 'ец'),
            (['абзац', 'агнец'], 'ц'),
        )
        for expected, postfix in params:
            with self.subTest(f'Test starts with {postfix}'):
                word = Word(5)
                word.cached = DATA
                word.ends_with(postfix)
                result = word.examples(5)
                self.assertEqual(expected, result)

    def test_ends_and_starts_with_works(self):
        word = Word(5)
        word.cached = DATA
        word.starts_with('АГ')
        word.ends_with('ец')
        result = word.examples(5)
        self.assertEqual(['агнец'], result)


if __name__ == '__main__':
    main()
