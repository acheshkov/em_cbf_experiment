# import re
# from typing import List, Tuple, Dict, Optional


class Range:
    ''' Line range from a to b includes a and b and start from zero'''
    def __init__(self, start: int, end: int = None):
        self._start = start
        self._end = end or start
        assert self._start <= self._end

    @staticmethod
    def from_str(s: str) -> 'Range':
        if isinstance(s, list):
            start, end = s
        else:
            start, end = eval(s)
        return Range(start, end)

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'[{self._start},{self._end}]'

    def __eq__(self, other: 'Range'):
        return self._start == other._start and self._end == other._end

    def contains(self, range: 'Range') -> bool:
        return self._start <= range.start and self._end >= range.end
