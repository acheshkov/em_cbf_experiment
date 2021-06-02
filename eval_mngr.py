from ranked_list import RankedList
from line_range import Range
from typing import List
import pandas as pd
import numpy as np


class EvalMngr:
    def __init__(self, alpha=3, max_list_len=20):
        self._alpha = alpha
        self._max_list_len = max_list_len

    def utility(self, ranked_list: RankedList) -> float:
        sum = 0
        num = 1
        true_positions = list(filter(
            lambda v: v <= self._max_list_len,
            ranked_list.true_positions
        ))
        for v in true_positions:
            num = 1
            den = 2 ** ((v - 1) / (self._alpha - 1))
            sum += num / den
        return sum

    def max_utility(self, ranked_list: RankedList, default=1) -> float:
        if len(ranked_list.true_positions) == 0:
            return default

        df = pd.DataFrame(
            [(i, True) for i, v in enumerate(ranked_list.true_positions)],
            columns=['score', 'is_true']
        )
        best_ranked_list = RankedList(df)
        return self.utility(best_ranked_list)

    def r_score(self, rls: List[RankedList]) -> float:
        sum_num = 0
        sum_den = 0
        for rl in rls:
            sum_num += self.utility(rl)
            sum_den += self.max_utility(rl)
        return sum_num / sum_den

    def accuracy(self, rls: List[RankedList], top_k=1) -> float:
        sum = 0
        for rl in rls:
            if len(list(filter(lambda v: v <= top_k, rl.true_positions))) > 0:
                sum += 1
        return sum / len(rls)

    def jaccard(self, rls: List[RankedList], top_k=1) -> float:
        res = []
        for rl in rls:
            res.append(self._jaccard_rl(rl, top_k))
        return np.mean(res)

    def _jaccard(self, r1: Range, r2: Range) -> float:
        a = set(range(r1.start, r1.end + 1))
        b = set(range(r2.start, r2.end + 1))
        return len(a & b) / len(a | b)

    def _jaccard_rl(self, rl: RankedList, top_k=1) -> float:
        df: pd.DataFrame = rl.get()
        assert 'range' in df.columns
        assert 'true_range' in df.columns

        res = []
        for x, y in df[['range', 'true_range']][0: top_k].values:
            r1 = Range.from_str(x)
            r2 = Range.from_str(y)
            res.append(self._jaccard(r1, r2))

        return np.max(res, initial=0.0)
