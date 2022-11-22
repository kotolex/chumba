from enum import Enum
from pathlib import Path
from typing import List, Union


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
