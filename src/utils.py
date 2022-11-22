from enum import Enum
from pathlib import Path
from typing import List


class Lang(Enum):
    RU = 'ru'
    EN = 'en'


def read_file(lang: str) -> List[str]:
    real_path = Path(__file__).parent
    file_name = real_path / 'data' / f'words_{lang}.txt'
    with open(file_name, encoding='utf-8') as file:
        return [e.rstrip() for e in file]
