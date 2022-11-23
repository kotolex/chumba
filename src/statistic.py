import re
from collections import Counter
from typing import List, Tuple

from src.utils import from_generator


class Statistics:
    def __init__(self, content: str, ignored='-1234567890'):
        """
        Creates statistic object for given text, lower it, parse it for words by spaces and ignoring punctuation.
        If words in sequence ignored, then it won't be in resulting statistics.
        For example, if '-' in ignored argument, then word '-' will not appear at results
        :param content: string representation of some text
        :param ignored: sequence for ignore words
        """
        self.words = [e for e in re.split(r"[^\w'-]+", content) if e and e not in ignored]
        self.words_count = len(self.words)
        self.counter = Counter(e.lower() for e in self.words)
        self.unique_words = list(self.counter.keys())
        self.unique_words_count = len(self.unique_words)

    def most_common(self, limit: int = 0) -> List[Tuple]:
        """
        Returns list of pairs(tuples) of most common words in text, like [('word', word_count_in_text)].
        For example, for text 'a a a b b' it will be [('a', 3), ('b', 2)]
        Limit argument limiting result, if it is less or equal zero - all results will be return, but limit can be
        bigger, than actual results count
        Analog (wrapper) of Counter.most_common
        :param limit: how many words should be in result
        :return: list of pairs word-count
        """
        if limit <= 0:
            limit = None
        return self.counter.most_common(limit)

    def less_common(self, limit: int = 0) -> List[Tuple]:
        """
        Returns list of pairs(tuples) of less common words in text, like [('word', word_count_in_text)].
        Reverse of most_common method.
        For example, for text 'a a a b b c' it will be [('c', 1), ('b', 2), ('a', 3)]
        Limit argument limiting result, if it is less or equal zero - all results will be return, but limit can be
        bigger, than actual results count
        :param limit: how many words should be in result
        :return: list of pairs word-count
        """
        results = reversed(self.counter.most_common())
        return from_generator(results, limit)

    def words_with_count(self, count: int, *, limit: int = 0) -> List[str]:
        """
        Returns list  of words(strings) with given count in text.
        For example, for text 'a a a b b c'  words_with_count(1)  will be ['c']
        Limit argument limiting result, if it is less or equal zero - all results will be return, but limit can be
        bigger, than actual results count
        :param count: how many times word appears in given text
        :param limit: how many words should be in result
        :return: list of strings
        """
        results = (a for a, b in self.counter.items() if b == count)
        return from_generator(results, limit)

    def words_with_length(self, length: int, *, limit: int = 0):
        """
        Returns list  of words(strings) with given length in text.
        For example, for text 'a a a bb bb ccc' words_with_length(2) will be ['bb']
        Limit argument limiting result, if it is less or equal zero - all results will be return, but limit can be
        bigger, than actual results count
        :param length: length of word to find
        :param limit: how many words should be in result
        :return: list of strings
        """
        results = (a for a in self.counter.keys() if len(a) == length)
        return from_generator(results, limit)

    def __repr__(self):
        return f'Text statistic: words count={self.words_count}, unique words count={self.unique_words_count}, ' \
               f'3 most common words={self.most_common(3)}, 3 less common words={self.less_common(3)}'
