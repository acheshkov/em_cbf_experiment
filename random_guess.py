import pandas as pd
from inference_results import InferenceResults
from ranked_list import RankedList
import random
from typing import Tuple, List
from utils import Range


class RandomGuessModel:
    def recommend(self, vs: List[Tuple[bool, Range, Range]]) -> RankedList:
        shuffled = [(rank, ) + value for rank, value in zip(range(1, len(vs) + 1), random.sample(vs, len(vs)))]

        return RankedList(pd.DataFrame(
            shuffled,
            columns=['score', 'is_true', 'range', 'true_range']
        ))


def inference_random_guess(model: RandomGuessModel, data: pd.DataFrame) -> InferenceResults:
    pass
