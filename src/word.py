from typing import List


class Word:
    RU = 'ru'
    EN = 'en'

    def __init__(self, length: int, ru=True):
        """
        Create instance of word wrapper
        :param length: length of the search word
        :param ru: lang of the dictionary to look in
        """
        self.length = length
        self.dictionary = Word.RU if ru else Word.EN
        self.cached = []

    def examples(self, limit: int = 1) -> List[str]:
        """
        Returns all results matching the conditions, limited if necessary by limit keyword. If limit is less or equal
        zero, then all results will be given
        :param limit: size of the resulting list, if <=0 then all results
        :return: list of string results
        """
        if not self.cached:
            self._read_all(self.dictionary)
        return [e for e in self.cached if self.length == len(e)][:limit]

    def letter_at_index_is(self, index: int, letter: str):
        pass

    def starts_with(self, prefix: str):
        pass

    def ends_with(self, postfix: str):
        pass

    def examples_count(self) -> int:
        pass

    def _read_all(self, lang: str):
        file_name = f'./data/words_{lang}.txt'
        with open(file_name, encoding='utf-8') as file:
            self.cached = [e.rstrip() for e in file]


if __name__ == '__main__':
    word = Word(5)
    print(word.examples(15))
