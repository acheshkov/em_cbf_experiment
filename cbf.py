import pandas as pd
from inference_results import InferenceResults


@dataclass
class CBFModel:
    pass



def train_cbf_model_per_project(dataset: pd.DataFrame) -> CBFModel:
    pass

def train_cbf_model_global(dataset: pd.DataFrame) -> CBFModel:
    pass

def inference_cbf(model: CBFModel, data: pd.DataFrame) -> InferenceResults:
    pass