from config import Config
from typing import Dict
from type_aliases import ModelName
from eval_results import EvalResults
from dataset import get_dataset, split_dataset 
from cbf import train_cbf_model_per_project, train_cbf_model_single
from cbf import inference_cbf
from semi import inference_semi
from eval_results import eval_recommender

def pipeline(config: Config, n=None) -> Dict[ModelName, EvalResults]:
    dataset = get_dataset(config, n)
    train, test = split_dataset(dataset, random_state=42)
    
    model_per_project = train_cbf_model_per_project(train)
    model_single = train_cbf_model_single(train)
    
    result_cbf_per_project = inference_cbf(model_per_project, test)
    result_cbf_single = inference_cbf(model_single, test)
    result_semi = inference_semi(test)
    
    perf_cbf_per_project = eval_recommender(model_per_project)
    perf_cbf_single = eval_recommender(model_single)
    perf_semi = eval_recommender(result_semi)
    
    return {
        "cbf_code2vec_many": perf_cbf_per_project,
        "cbf_code2vec_single": perf_cbf_single,
        "SEMI": perf_semi
    }

