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


def _inference(g: pd.DataFrame, predictions: InferenceResults, model: RandomGuessModel) -> None:
    xs = g[['is_true_emo', 'range', 'true_range']].values.tolist()
    xs = [(b, r, tr) for (b, r, tr) in xs]
    recommendation = model.recommend(xs)
    predictions.add('*', recommendation)


def inference_random_guess(model: RandomGuessModel, data: pd.DataFrame) -> InferenceResults:
    columns = ['filename', 'is_true_emo']
    for col in columns:
        assert col in data.columns

    predictions = InferenceResults()
    data.groupby('filename').apply(lambda g: _inference(g, predictions, model))
    return predictions
