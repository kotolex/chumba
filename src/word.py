from typing import List, Tuple


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
        Returns all results matching the predefined conditions, limited if necessary by limit keyword. If limit is less
        or equal zero, then all results will be given
        :param limit: size of the resulting list, if <=0 then all results
        :return: list of string results
        """
        if not self.cached:
            self._read_all(self.dictionary)
        results = self._apply_all_conditions()
        if limit <= 0:
            return results
        return results[:limit]

    def letter_at_index_is(self, index: int, letter: str) -> None:
        """
        Adds condition, that search word is contains given letter on given index. Index starts with 0 (not 1).
        Index cant be smaller, than 0 or bigger, than length of the word. Letter should be a string with length=1
        :param index: index of letter in range (0, len(word))
        :param letter: exactly one letter
        :return: None
        :raises ValueError if index is wrong or length of the letter bigger than 1
        """
        if index < 0 or index > self.length - 1:
            raise ValueError(f'Index should be in range (0,{self.length})')
        if len(letter) != 1:
            raise ValueError(f'Letter should have length 1, got {len(letter)}')
        letter = letter.lower()
        self.conditions.append(lambda w: w[index] == letter)

    def starts_with(self, prefix: str) -> None:
        """
        Adds condition, that search word is starts with prefix. Prefix cant be bigger, than word itself
        :param prefix: starting part of search word
        :return: None
        :raises ValueError if length of the prefix is bigger than length of the word
        """
        self._starts_ends(prefix, is_starts=True)

    def ends_with(self, postfix: str):
        """
        Adds condition, that search word is ends with postfix. Postfix cant be bigger, than word itself
        :param postfix: ending part of the search word
        :return: None
        :raises ValueError if length of the postfix is bigger than length of the word
        """
        self._starts_ends(postfix, is_starts=False)

    def contains(self, *letters: str) -> None:
        """
        Adds condition, that search word contains given letters. Each letter should be a string with length=1
        :param letters: parameters, each of this are exactly one letter
        :return: None
        :raises ValueError if length of some letter not equal 1
        """
        self._contains(letters, is_contains=True)

    def not_contains(self, *letters: str) -> None:
        """
        Adds condition, that search word not contains given letters. Each letter should be a string with length=1
        :param letters: parameters, each of them are exactly one letter
        :return: None
        :raises ValueError if length of some letter not equal 1
        """
        self._contains(letters, is_contains=False)

    def examples_count(self) -> int:
        pass

    def _read_all(self, lang: str) -> None:
        file_name = f'./data/words_{lang}.txt'
        with open(file_name, encoding='utf-8') as file:
            self.cached = [e.rstrip() for e in file]

    def _apply_all_conditions(self) -> List[str]:
        return [e for e in self.cached if all(condition(e) for condition in self.conditions)]

    def _contains(self, letters: Tuple[str], is_contains: bool = True) -> None:
        for letter in letters:
            if len(letter) != 1:
                raise ValueError(f'Letter should have length 1, got {len(letter)}')
        for letter in letters:
            letter = letter.lower()
            if is_contains:
                self.conditions.append(lambda w: letter in w)
            else:
                self.conditions.append(lambda w: letter not in w)

    def _starts_ends(self, fix: str, is_starts: bool = True) -> None:
        fix_name = 'Prefix' if is_starts else 'Postfix'
        if len(fix) > self.length:
            raise ValueError(f'{fix_name} {fix} is bigger than word length({self.length})')
        if not fix:
            return None
        fix = fix.lower()
        if is_starts:
            self.conditions.append(lambda w: w.startswith(fix))
        else:
            self.conditions.append(lambda w: w.endswith(fix))
