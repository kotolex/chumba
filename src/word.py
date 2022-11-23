from typing import List, Tuple, Callable, Generator

from src.utils import from_generator, read_data_file, Lang


class Word:

    def __init__(self, length: int = 0, is_ru=True):
        """
        Create instance of word wrapper - a tool to search for word in dictionaries with various conditions.
        :param length: length of the searched word, if it less or equals to zero - word of any length will be searched
        :param is_ru: is lang of the dictionary to look in is Russian, will be English if False
        """
        self._length: int = length if length > 0 else 0
        self._lang: str = str(Lang.RU.value) if is_ru else str(Lang.EN.value)
        self._cached: List[str] = []
        self._conditions: List[Callable] = [lambda w: len(w) == self._length] if self._length else []

    def examples(self, limit: int = 0) -> List[str]:
        """
        Returns all results matching the predefined conditions, limited if necessary by limit keyword. If limit is less
        or equal zero, then all results will be given
        :param limit: size of the resulting list, if <= 0 then all results
        :return: list of string results
        """
        if not self._cached:
            self._read_all(self._lang)
        results = self._apply_all_conditions()
        return from_generator(results, limit)

    def letter_at_index_is(self, index: int, letter: str) -> None:
        """
        Adds condition, that search word is contains given letter on given index. Index starts with 0 (not 1).
        Index cant be smaller, than 0 or bigger, than length of the word. Letter should be a string with length=1
        :param index: index of letter in range (0, len(word))
        :param letter: exactly one letter
        :return: None
        :raises ValueError if index is wrong or length of the letter bigger than 1
        """
        if index < 0 or (self._length and index > self._length - 1):
            raise ValueError(f'Index should be in range (0, {self._length})')
        if len(letter) != 1:
            raise ValueError(f'Letter should have length 1, got {len(letter)}')
        letter = letter.lower()
        self._conditions.append(lambda w: w[index] == letter)

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
        """
        Returns number of words, which are matched with all conditions. If there are no conditions yet, then returns
        count of words in current dictionary
        :return: number of found words (examples)
        """
        _results = self.examples(limit=-1)
        return len(_results)

    def _read_all(self, lang: str) -> None:
        self._cached = read_data_file(lang)

    def _apply_all_conditions(self) -> Generator:
        return (e for e in self._cached if all(condition(e) for condition in self._conditions))

    def _contains(self, letters: Tuple[str], is_contains: bool = True) -> None:
        for letter in letters:
            if len(letter) != 1:
                raise ValueError(f'Letter should have length 1, got {len(letter)}')
        for letter in letters:
            letter = letter.lower()
            if is_contains:
                self._conditions.append(lambda w: letter in w)
            else:
                self._conditions.append(lambda w: letter not in w)

    def _starts_ends(self, fix: str, is_starts: bool = True) -> None:
        fix_name = 'Prefix' if is_starts else 'Postfix'
        if 0 < self._length < len(fix):
            raise ValueError(f'{fix_name} {fix} is bigger than word length({self._length})')
        if fix:
            fix = fix.lower()
            if is_starts:
                self._conditions.append(lambda w: w.startswith(fix))
            else:
                self._conditions.append(lambda w: w.endswith(fix))
