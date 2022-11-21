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
        self.conditions = [lambda w: len(w) == self.length]

    def examples(self, limit: int = 1) -> List[str]:
        """
        Returns all results matching the conditions, limited if necessary by limit keyword. If limit is less or equal
        zero, then all results will be given
        :param limit: size of the resulting list, if <=0 then all results
        :return: list of string results
        """
        if not self.cached:
            self._read_all(self.dictionary)
        results = self._apply_all_conditions()
        if limit <= 0:
            return results
        return results[:limit]

    def letter_at_index_is(self, index: int, letter: str):
        pass

    def starts_with(self, prefix: str) -> None:
        """
        Adds condition, that search word is starts with prefix. Prefix cant be bigger, than word itself
        :param prefix: starting part of search word
        :return: None
        :raises ValueError if length of the prefix is bigger than length of the word
        """
        if len(prefix) > self.length:
            raise ValueError(f'Prefix {prefix} is bigger than word length({self.length})')
        if not prefix:
            return None
        prefix = prefix.lower()
        self.conditions.append(lambda w: w.startswith(prefix))

    def ends_with(self, postfix: str):
        """
        Adds condition, that search word is ends with postfix. Postfix cant be bigger, than word itself
        :param postfix: ending part of the search word
        :return: None
        :raises ValueError if length of the postfix is bigger than length of the word
        """
        if len(postfix) > self.length:
            raise ValueError(f'Postfix {postfix} is bigger than word length({self.length})')
        if not postfix:
            return None
        postfix = postfix.lower()
        self.conditions.append(lambda w: w.endswith(postfix))

    def examples_count(self) -> int:
        pass

    def _read_all(self, lang: str):
        file_name = f'./data/words_{lang}.txt'
        with open(file_name, encoding='utf-8') as file:
            self.cached = [e.rstrip() for e in file]

    def _apply_all_conditions(self) -> List[str]:
        return [e for e in self.cached if all(condition(e) for condition in self.conditions)]
