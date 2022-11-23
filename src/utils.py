from enum import Enum
from itertools import islice
from pathlib import Path
from typing import List, Union, Generator, Any


class Lang(Enum):
    RU = 'ru'
    EN = 'en'


def read_data_file(lang: str, encoding='utf-8') -> List[str]:
    real_path = Path(__file__).parent
    file_name = real_path / 'data' / f'words_{lang}.txt'
    return [e.rstrip() for e in read_file(file_name, encoding)]


def read_file(file_name: Union[Path, str], encoding='utf-8') -> List[str]:
    with open(file_name, encoding=encoding) as file:
        return list(file)


def from_generator(gen: Union[Generator, reversed], limit: int) -> List[Any]:
    if limit <= 0:
        return list(gen)
    return list(islice(gen, limit))
