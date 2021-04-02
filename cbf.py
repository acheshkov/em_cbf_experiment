from dataclasses import dataclass, field
import pandas as pd
import numpy as np
from inference_results import InferenceResults
from typing import Dict, List, Tuple, Optional
from type_aliases import Vector, ProjectName
from ranked_list import RankedList
from line_range import Range
from scipy.spatial.distance import cosine


@dataclass
class CBFModel:
    profiles_sources: Dict[ProjectName, List[Vector]] = field(default_factory=dict, init=False)
    profiles: Dict[ProjectName, Vector] = field(default_factory=dict, init=False)

    def add(self, project_key: ProjectName, vector: Vector) -> None:
        if project_key not in self.profiles_sources:
            self.profiles_sources[project_key] = []
        self.profiles_sources[project_key].append(vector)

    def cos_dist(self, project_key: ProjectName, v: Vector) -> float:
        user_profile = self.profiles[project_key]
        return cosine(user_profile, v)

    def train(self) -> None:
        for project in self.profiles_sources:
            self.profiles[project] = np.array(self.profiles_sources[project]).mean(axis=0)

    def recommend(self, vs: List[Tuple[Vector, bool, Range, Range]], project: ProjectName) -> Optional[RankedList]:
        if project not in self.profiles:
            return None
        data = [(self.cos_dist(project, v), t, str(r), str(tr)) for v, t, r, tr in vs]
        df = pd.DataFrame(data, columns=['d', 'is_true', 'range', 'true_range'])
        df['rank'] = df['d'].rank(pct=True, ascending=True)
        return RankedList(df[['rank', 'is_true', 'range', 'true_range']], 'rank', 'is_true')


def train_cbf_model_per_project(dataset: pd.DataFrame) -> CBFModel:
    pass


def train_cbf_model_single(dataset: pd.DataFrame) -> CBFModel:
    pass


def inference_cbf(model: CBFModel, data: pd.DataFrame) -> InferenceResults:
    pass
