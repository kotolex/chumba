from enum import Enum
from itertools import islice
from pathlib import Path
from typing import List, Union, Generator, Any


class Lang(Enum):
    """
    Language enumerator for using in Word class
    """
    RU = 'ru'
    EN = 'en'


def read_data_file(lang: str, encoding='utf-8') -> List[str]:
    """
    Reads dictionary file from data folder which is in same folder as this module. For internal use.
    Will be look for template 'words_lang.txt' there, reads it with given encoding and return list of stripped lines
    :param lang: ru or en for dictionary
    :param encoding: encoding for reading, UTF-8 by default
    :return: list of lines(strings)
    """
    real_path = Path(__file__).parent
    file_name = real_path / 'data' / f'words_{lang}.txt'
    return [e.rstrip() for e in read_file(file_name, encoding)]


def read_file(file_name: Union[Path, str], encoding='utf-8') -> List[str]:
    """
    Reads file from given path, specified in file_name (Path or string) and returns all lines unchanged
    :param file_name: Path or file_name(full path)
    :param encoding: encoding for reading, UTF-8 by default
    :return: list of lines(strings)
    """
    with open(file_name, encoding=encoding) as file:
        return list(file)


def from_generator(gen: Union[Generator, reversed], limit: int) -> List[Any]:
    """
    Gets a generator/iterator and will return as many results as in limit argument. If a generator wraps a big content
    it will be convenient to use this function to save space.
    If limit is less or equal zero, or limit bigger, than wrapped container -all results will be returned
    :param gen: generator or iterator of some container
    :param limit: how many results to return from generator
    :return: list of results
    """
    if limit <= 0:
        return list(gen)
    return list(islice(gen, limit))
