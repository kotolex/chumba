from unittest import TestCase, main
from src.word import Word


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


if __name__ == '__main__':
    main()
