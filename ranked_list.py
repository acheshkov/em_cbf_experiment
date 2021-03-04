import pandas as pd
from typing import List, Tuple


class RankedList:
    def __init__(self, data: pd.DataFrame, score='score', is_true='is_true', rnd=False):
        assert score in data.columns
        assert is_true in data.columns
        sorted_asc = data.sort_values(by=score).reset_index(drop=True)
        self._score_column = score
        self._is_true_column = is_true
        self._size = len(data)
        self._true_pos_idxs = (sorted_asc.query(f'{self._is_true_column} == True').index + 1).tolist()

    @staticmethod
    def from_list(data: List[Tuple[float, bool]], score='score', is_true='is_true') -> 'RankedList':
        return RankedList(
          pd.DataFrame(data, columns=['score', 'is_true'])
        )

    @property
    def true_positions(self) -> List[int]:
        return self._true_pos_idxs
