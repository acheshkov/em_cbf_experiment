from dataclasses import dataclass, field
from inference_results import InferenceResults
from type_aliases import ProjectName
from eval_mngr import EvalMngr
from ranked_list import RankedList
from typing import Tuple, List, Any, Dict

Metric = float


@dataclass
class EvalResults:
    results: Dict[ProjectName, Any] = field(default_factory=dict, init=False)

    def evaluate(self, inference_data: InferenceResults) -> None:
        rcmds = inference_data.recommendations
        for group in rcmds:
            self.results[group] = self._eval(rcmds[group])

    def _eval(self, rls: List[RankedList]) -> Tuple[Metric, Metric, Metric, Metric, Metric, Metric]:
        mgr = EvalMngr()
        r_score = round(mgr.r_score(rls), 3)
        acc_1 = round(mgr.accuracy(rls, top_k=1), 3)
        acc_3 = round(mgr.accuracy(rls, top_k=3), 3)
        acc_5 = round(mgr.accuracy(rls, top_k=5), 3)
        iou_1 = round(mgr.jaccard(rls, top_k=1), 3)
        iou_3 = round(mgr.jaccard(rls, top_k=3), 3)
        return r_score, acc_1, acc_3, acc_5, iou_1, iou_3


def eval_recommender(inference_data: InferenceResults) -> EvalResults:
    er = EvalResults()
    er.evaluate(inference_data)
    return er
