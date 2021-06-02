from dataclasses import dataclass, field
from type_aliases import ProjectName
from ranked_list import RankedList
from typing import Dict, List


@dataclass
class InferenceResults:
    recommendations: Dict[ProjectName, List[RankedList]] = field(default_factory=dict, init=False)

    def add(self, project_key, rl: RankedList):
        if project_key not in self.recommendations:
            self.recommendations[project_key] = []
        self.recommendations[project_key].append(rl)

    def flat(self, group_name='*') -> 'InferenceResults':
        ''' To merge all groups into one'''
        er = InferenceResults()
        for key in self.recommendations:
            for rl in self.recommendations[key]:
                er.add(group_name, rl)
        return er
