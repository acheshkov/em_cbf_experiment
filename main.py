from config import Config
from typing import Dict
from type_aliases import ModelName
from eval_results import EvalResults
from dataset import get_dataset, split_dataset
from cbf import train_cbf_model_per_project, train_cbf_model_single
from cbf import inference_cbf, inference_cbf_single
from semi import inference_semi
from eval_results import eval_recommender
from random_guess import RandomGuessModel, inference_random_guess


def pipeline(config: Config) -> Dict[ModelName, EvalResults]:
    dataset = get_dataset(config)
    train, test = split_dataset(dataset, random_state=42)

    model_per_project = train_cbf_model_per_project(train)
    model_global = train_cbf_model_single(train)
    model_random = RandomGuessModel()

    result_cbf_per_project = inference_cbf(model_per_project, test)
    result_cbf_global = inference_cbf_single(model_global, test)
    result_semi = inference_semi(test, config)
    result_random_guess = inference_random_guess(model_random, test)

    perf_cbf_per_project = eval_recommender(result_cbf_per_project.flat())
    perf_cbf_single = eval_recommender(result_cbf_global)
    perf_semi = eval_recommender(result_semi)
    perf_random_guess = eval_recommender(result_random_guess)

    return {
        "cbf_code2vec_many": perf_cbf_per_project,
        "cbf_code2vec_single": perf_cbf_single,
        "SEMI": perf_semi,
        'random_guess': perf_random_guess
    }
