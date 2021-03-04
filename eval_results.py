from dataclasses import dataclass
from inference_results import InferenceResults


@dataclass
class EvalResults:
    pass


def eval_recommender(inference_data: InferenceResults) -> EvalResults:
    pass
