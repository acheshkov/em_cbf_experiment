
import pandas as pd
import os
import subprocess
import tempfile
from inference_results import InferenceResults
from prepare_data_for_semi_eval import prepare_semi_data
from config import Config
from dataset import get_synth_dataset
from ranked_list import RankedList
from semi_utils import semi_recommendation_str_to_list


def run_semi_algorithm(df: pd.DataFrame, config: Config) -> pd.DataFrame:
    '''Run SEMI inference using provided execuatable'''
    with tempfile.NamedTemporaryFile() as tmp, tempfile.NamedTemporaryFile() as semi_out:
        df.to_csv(tmp.name, header=False, sep=';', index=False)
        _ = subprocess.run([
            'java', '-jar',
            config.path_to_semi_jar,
            tmp.name,
            semi_out.name
        ], capture_output=True, text=True)
        # out = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        semi_df = pd.read_csv(semi_out.name, sep=';', names=['filename', 'method', 'semi_recommendations'])
        semi_df.semi_recommendations = semi_df.semi_recommendations.apply(semi_recommendation_str_to_list)
        semi_df.filename = semi_df.filename.apply(os.path.basename)
        return semi_df


def _calclualte_inference_data_for_semi(data: pd.DataFrame, path_to_java_files: str) -> pd.DataFrame:
    ''' To read pre calculated data '''
    columns = ['filename', 'target_method', 'target_method_start_line']
    for c in columns:
        assert c in data.columns, f"Can't find column: {c}"

    # data = data.astype({'target_method_start_line': 'int32'}) # TODO: move
    df, err_count = prepare_semi_data(
        data.groupby(columns).size().reset_index()[columns].values,
        path_to_java_files
    )
    print('SEMI data prepare error count:', err_count)
    return df


def _get_semi_inference_from_file_or_calclulate(data: pd.DataFrame, config: Config) -> pd.DataFrame:
    if config.path_to_semi_inference_csv is not None:
        print('Load precomputed SEMI inference.')
        semi_df = pd.read_csv(config.path_to_semi_inference_csv, sep=';')
        filenames_filter = [os.path.basename(fn) for fn in data.filename.unique()]
        semi_df = semi_df.merge(pd.DataFrame(filenames_filter, columns=['filename']), on='filename')
    else:
        print('Precomputed SEMO inference file is not found. It will be calculated from scratch')
        df = _calclualte_inference_data_for_semi(data, config.path_to_java_files)
        semi_df = run_semi_algorithm(df)
        semi_df.to_csv(config.path_to_semi_inference_csv, sep=';', index=False)
    return semi_df


def _preprocess_data(data: pd.DataFrame, config: Config) -> pd.DataFrame:
    semi_df = _get_semi_inference_from_file_or_calclulate(data, config)
    synth_dataset = get_synth_dataset(config.path_to_dataset, config.path_to_java_files)
    join = semi_df.merge(synth_dataset, 'right', left_on='filename', right_on='filename')
    join.semi_recommendations.fillna('[]', inplace=True)
    join.semi_recommendations = join.semi_recommendations.apply(eval)
    semi_data = join[['semi_recommendations', 'true_inline_range', 'filename']].values
    return semi_data


def inference_semi(data: pd.DataFrame, config: Config) -> InferenceResults:
    semi_data = _preprocess_data(data, config)

    predictions = InferenceResults()
    for recommendations, y, fn in semi_data:
        recommendations = [rng for rng, score in recommendations if (score >= 0 and (rng[0] <= rng[1]))]
        if len(recommendations) == 0:
            predictions.add('*', RankedList(pd.DataFrame([], columns=['score', 'is_true', 'range', 'true_range'])))
            continue
        y = eval(y)
        y = [y[0] + 1, y[1] + 1]
        rl = RankedList(pd.DataFrame(
            [(i + 1, x == y, str(x), str(y)) for i, x in enumerate(recommendations)],
            columns=['score', 'is_true', 'range', 'true_range']
        ))

        predictions.add('*', rl)

    return predictions
