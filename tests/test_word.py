from unittest import TestCase, main

from src.word import Word, Lang

DATA = ['ёкать', 'ёмкий', 'ёрник', 'аббат', 'абзац', 'аборт', 'абрек', 'абрис', 'авизо', 'аврал', 'автол', 'агент',
        'агнец', 'адепт', 'адрес']


class TestWord(TestCase):
    def test_simple_object(self):
        word = Word(10)
        self.assertEqual(word._cached, [])
        self.assertEqual(word._length, 10)
        self.assertEqual(word._lang, Lang.RU.value)

    def test_en_dict(self):
        word = Word(10, False)
        self.assertEqual(word._cached, [])
        self.assertEqual(word._length, 10)
        self.assertEqual(word._lang, Lang.EN.value)

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
                word._cached = DATA
                result = word.examples(limit)
                self.assertEqual(expected, result)

    def test_starts_with_raises_when_bigger_than_length(self):
        word = Word(1)
        with self.assertRaises(ValueError) as e:
            word.starts_with('22')
        self.assertEqual(str(e.exception), "Prefix 22 is bigger than word length(1)")

    def test_starts_with_do_nothing_when_empty(self):
        word = Word(1)
        cond = word._conditions[:]
        word.starts_with('')
        self.assertEqual(cond, word._conditions)

    def test_starts_with_appends_to_conditions(self):
        word = Word(12)
        cond = word._conditions[:]
        word.starts_with('12')
        self.assertEqual(len(cond) + 1, len(word._conditions))

    def test_ends_with_raises_when_bigger_than_length(self):
        word = Word(1)
        with self.assertRaises(ValueError) as e:
            word.ends_with('22')
        self.assertEqual(str(e.exception), "Postfix 22 is bigger than word length(1)")

    def test_ends_with_do_nothing_when_empty(self):
        word = Word(1)
        cond = word._conditions[:]
        word.ends_with('')
        self.assertEqual(cond, word._conditions)

    def test_ends_with_appends_to_conditions(self):
        word = Word(12)
        cond = word._conditions[:]
        word.ends_with('12')
        self.assertEqual(len(cond) + 1, len(word._conditions))

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
                word._cached = DATA
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
                word._cached = DATA
                word.ends_with(postfix)
                result = word.examples(5)
                self.assertEqual(expected, result)

    def test_ends_and_starts_with_works(self):
        word = Word(5)
        word._cached = DATA
        word.starts_with('АГ')
        word.ends_with('ец')
        result = word.examples(5)
        self.assertEqual(['агнец'], result)

    def test_letter_at_index_is_raises_when_small_index(self):
        word = Word(12)
        with self.assertRaises(ValueError) as e:
            word.letter_at_index_is(-1, '2')
        self.assertEqual(str(e.exception), "Index should be in range (0, 12)")

    def test_letter_at_index_is_raises_when_big_index(self):
        word = Word(5)
        with self.assertRaises(ValueError) as e:
            word.letter_at_index_is(5, '2')
        self.assertEqual(str(e.exception), "Index should be in range (0, 5)")

    def test_letter_at_index_is_raises_when_letter_is_not_single(self):
        word = Word(12)
        with self.assertRaises(ValueError) as e:
            word.letter_at_index_is(3, '22')
        self.assertEqual(str(e.exception), "Letter should have length 1, got 2")

    def test_letter_at_index_is_raises_when_letter_is_empty(self):
        word = Word(12)
        with self.assertRaises(ValueError) as e:
            word.letter_at_index_is(3, '')
        self.assertEqual(str(e.exception), "Letter should have length 1, got 0")

    def test_letter_at_index_is(self):
        params = (
            (['авизо', 'аврал', 'автол'], 1, 'В'),
            (['авизо', 'аврал', 'автол'], 1, 'в'),
            (['аббат', 'абзац', 'аборт', 'абрек', 'абрис'], 1, 'б'),
            (['ёрник', 'абрек'], 4, 'к'),
            ([], 1, 'w'),
        )
        for expected, index, letter in params:
            with self.subTest(f'Test letter at index {index} is {letter}'):
                word = Word(5)
                word._cached = DATA
                word.letter_at_index_is(index, letter)
                result = word.examples(5)
                self.assertEqual(expected, result)

    def test_three_conditions(self):
        word = Word(5)
        word._cached = DATA
        word.starts_with('АГ')
        word.ends_with('ец')
        word.letter_at_index_is(2, 'н')
        result = word.examples(5)
        self.assertEqual(['агнец'], result)

    def test_contains_raises_if_letter_is_empty(self):
        word = Word(12)
        with self.assertRaises(ValueError) as e:
            word.contains('')
        self.assertEqual(str(e.exception), "Letter should have length 1, got 0")

    def test_contains_is_raises_when_letter_is_not_single(self):
        word = Word(12)
        with self.assertRaises(ValueError) as e:
            word.contains('22')
        self.assertEqual(str(e.exception), "Letter should have length 1, got 2")

    def test_contains(self):
        params = (
            (['ёмкий', 'ёрник', 'абрис', 'авизо'], 'и'),
            (['ёкать', 'аббат', 'аборт', 'автол', 'агент'], 'т'),
            (['ёкать', 'аббат', 'абзац', 'аборт', 'абрек'], 'а'),
            ([], 'w'),
        )
        for expected, letter in params:
            with self.subTest(f'Test contains {letter}'):
                word = Word(5)
                word._cached = DATA
                word.contains(letter)
                result = word.examples(5)
                self.assertEqual(expected, result)

    def test_four_conditions(self):
        word = Word(5)
        word._cached = DATA
        word.starts_with('ё')
        word.ends_with('й')
        word.letter_at_index_is(2, 'к')
        word.contains('м', 'и')
        result = word.examples(5)
        self.assertEqual(['ёмкий'], result)

    def test_not_contains_raises_if_letter_is_empty(self):
        word = Word(12)
        with self.assertRaises(ValueError) as e:
            word.not_contains('')
        self.assertEqual(str(e.exception), "Letter should have length 1, got 0")

    def test_not_contains_is_raises_when_letter_is_not_single(self):
        word = Word(12)
        with self.assertRaises(ValueError) as e:
            word.not_contains('22')
        self.assertEqual(str(e.exception), "Letter should have length 1, got 2")

    def test_not_contains(self):
        params = (
            (['ёкать', 'аббат', 'абзац', 'аборт', 'абрек'], 'и'),
            (['ёмкий', 'ёрник', 'абзац', 'абрек', 'абрис'], 'т'),
            (['ёмкий', 'ёрник'], 'а'),
        )
        for expected, letter in params:
            with self.subTest(f'Test contains {letter}'):
                word = Word(5)
                word._cached = DATA
                word.not_contains(letter)
                result = word.examples(5)
                self.assertEqual(expected, result)

    def test_five_conditions(self):
        word = Word(5)
        word._cached = DATA
        word.starts_with('ё')
        word.ends_with('й')
        word.letter_at_index_is(2, 'к')
        word.contains('м', 'и')
        word.not_contains('ф', 'а')
        result = word.examples(5)
        self.assertEqual(['ёмкий'], result)

    def test_five_conditions_without_length(self):
        word = Word()
        word._cached = DATA
        word.starts_with('ё')
        word.ends_with('й')
        word.letter_at_index_is(2, 'к')
        word.contains('м', 'и')
        word.not_contains('ф', 'а')
        result = word.examples(5)
        self.assertEqual(['ёмкий'], result)

    def test_five_conditions_with_negative_length(self):
        word = Word(-1)
        word._cached = DATA + ['амортизация']
        word.starts_with('а')
        word.ends_with('я')
        word.contains('з')
        word.not_contains('ф', 'ж')
        word.letter_at_index_is(1, 'м')
        result = word.examples(5)
        self.assertEqual(['амортизация'], result)

    def test_examples_count(self):
        params = (
            (3, 'ё'),
            (12, 'А'),
            (0, 'W'),
            (15, None),
        )
        for expected, letter in params:
            with self.subTest(f'Test contains {letter}'):
                word = Word()
                word._cached = DATA
                if letter:
                    word.starts_with(letter)
                self.assertEqual(expected, word.examples_count())


if __name__ == '__main__':
    main()
