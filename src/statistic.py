import re
from collections import Counter

from src.utils import read_file


class Statistic:
    def __init__(self, content: str, ignored='-1234567890'):
        self.words = [e for e in re.split("[^\w'-]+", content) if e and e not in ignored]
        self.words_count = len(self.words)
        self.counter = Counter(e.lower() for e in self.words)
        self.unique_words = list(self.counter.keys())
        self.unique_words_count = len(self.unique_words)

    def most_common(self, limit=None):
        return self.counter.most_common(limit)

    def less_common(self, limit=None):
        results = reversed(self.counter.most_common())
        if not limit:
            return list(results)
        return list(results)[:limit]

    def words_with_count(self, count: int = 1):
        return [a for a, b in self.counter.items() if b == count]

    def __repr__(self):
        return f'Text statistic:\nwords count={self.words_count}, unique words count={self.unique_words_count},\n' \
               f'3 most common words={self.most_common(3)}, 3 less common words={self.less_common(3)}'


if __name__ == '__main__':
    gen = read_file('./data/text.txt')
    s = Statistic(''.join(gen))
    print(s.words)
    print(s.words_count)
    print(s.unique_words)
    print(s.unique_words_count)
    print(s.most_common())
    print(s)
    print(s.words_with_count(3))
