import pandas as pd
from typing import List, Tuple
import random


class RankedList:
    def __init__(self, data: pd.DataFrame, score='score', is_true='is_true', rnd=False):
        assert score in data.columns
        assert is_true in data.columns
        self.sorted_asc = data.sort_values(by=score).reset_index(drop=True)
        self._score_column = score
        self._is_true_column = is_true
        self._size = len(data)
        self._true_pos_idxs = (self.sorted_asc.query(f'{self._is_true_column} == True').index + 1).tolist()
        if rnd is True:
            self.shuffle_list()

    def get(self) -> pd.DataFrame:
        '''Return original dataframe sorted ASC by rank'''
        return self.sorted_asc

    def shuffle_list(self):
        self._true_pos_idxs = random.sample(
            range(1, self._size + 1),
            len(self._true_pos_idxs)
        )

    @staticmethod
    def from_list(data: List[Tuple[float, bool]], score='score', is_true='is_true') -> 'RankedList':
        return RankedList(
            pd.DataFrame(data, columns=['score', 'is_true'])
        )

    @property
    def true_positions(self) -> List[int]:
        return self._true_pos_idxs
