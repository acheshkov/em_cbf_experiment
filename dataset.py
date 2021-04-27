
import pandas as pd
import os
from config import Config
from typing import Tuple, Optional
from type_aliases import Path
from type_aliases import EmosVectorsDataset, SynthDataset, Dataset
from sklearn.model_selection import train_test_split
from source_code_utils import complement_range_file


def get_emos_vectors(path_to_csv: Path) -> EmosVectorsDataset:
    ''' Load and prepare dataset with EMOs and corresponding vectors'''
    def _mk_link_to_original_sample(filename) -> str:
        return '_'.join(filename.split('_')[0: 4]) + '.java'

    def _extract_range(filename) -> str:
        out = list(map(int, filename.replace('.java', '').split('_')[-2:]))
        return str(out)

    emos_vectors = pd \
        .read_csv(path_to_csv, header=None, names=['emo_uid', 'vector_str']) \
        .drop_duplicates(['emo_uid'], keep=False)
    emos_vectors.emo_uid = emos_vectors.emo_uid.apply(os.path.basename)
    emos_vectors['filename_origin'] = emos_vectors.emo_uid.apply(_mk_link_to_original_sample)
    emos_vectors['range'] = emos_vectors.emo_uid.apply(_extract_range)
    return emos_vectors


def _figure_out_true_inline_range(row: pd.core.series.Series) -> Optional[str]:
    '''Figure out and returns True range as a string'''
    start = int(row['insertion_start']) - 1
    end = int(row['insertion_end']) - 1
    return None
    if end < start:
        return None
    range = complement_range_file(
        row['output_filename'],
        start,
        end,
    )
    return str(range)


def _drop_duplicates_by_filename(df: pd.DataFrame) -> pd.DataFrame:
    ''' To drop rows if there are duplication by filename '''
    return df.copy().drop_duplicates(['output_filename'], keep=False)


def _drop_rows_with_undefined_true_range(df: pd.DataFrame) -> pd.DataFrame:
    ''' To drop rows where True EMO is undefined'''
    return df.copy().dropna(subset=['true_inline_range'])


def _mk_full_path_to_java_files(df: pd.DataFrame, path_to_java_files: str) -> pd.DataFrame:
    df = df.copy()
    df.output_filename = df.output_filename.apply(
        lambda v: f'{path_to_java_files}/{v}'
    )
    return df


def get_synth_dataset(path_to_dataset_csv: Path, path_to_java_files: Path) -> SynthDataset:
    ''' Load and prepare Synthetic Dataset'''
    columns = [
        'output_filename',
        'insertion_start',
        'insertion_end',
        'class_name',
        'target_method',
        'project_id',
        'target_method_start_line'
    ]

    df = pd.read_csv(path_to_dataset_csv, usecols=columns)
    df = _drop_duplicates_by_filename(df)
    df['filename'] = df.output_filename.apply(os.path.basename)
    df = _mk_full_path_to_java_files(df, path_to_java_files)
    df['true_inline_range'] = df.apply(lambda row: _figure_out_true_inline_range(row), axis=1)
    df = _drop_rows_with_undefined_true_range(df)
    return df


def combine_all_together(emos: EmosVectorsDataset, synth: SynthDataset) -> Dataset:
    columns = [
        'filename', 'true_inline_range',
        'output_filename', 'target_method', 'target_method_start_line',
        'project_id', 'vector_str', 'range', 'emo_uid'
    ]
    join = synth.merge(emos, 'inner', left_on='filename', right_on='filename_origin')[columns].values
    data = []

    for fn, true_range, fn_full, method, target_method_start_line, project, vector_str, rrange, emo_uid in join:
        is_true_range = true_range == rrange
        rrange = eval(rrange)
        data.append((
            fn_full, emo_uid, vector_str, project,
            is_true_range,
            rrange[1] - rrange[0],
            method, target_method_start_line,
            str(rrange), true_range
        ))

    columns = [
        'filename', 'emo_uid', 'vector', 'project', 'is_true_emo', 'range_len',
        'target_method', 'target_method_start_line', 'range', 'true_range'
    ]
    df = pd.DataFrame(data, columns=columns)
    df = df.astype({'target_method_start_line': 'int32'})
    return df


def get_dataset(config: Config) -> pd.DataFrame:
    '''Load, preprocess and combine all input data parts together to form a single dataset'''
    synth = get_synth_dataset(config.path_to_dataset_csv, config.path_to_java_files)
    print("Synth dataset:", len(synth))
    emos_vectors = get_emos_vectors(config.path_to_emos_vectors)
    print("EMOS vectors dataset:", len(emos_vectors))
    ds = combine_all_together(emos_vectors, synth)
    print("Final dataset:", len(ds))
    return ds


def split_dataset(df: pd.DataFrame, random_state: int = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    '''Split a dataset with stratification by project name'''
    train, test = train_test_split(
        df,
        stratify=df['project'].values.tolist(),
        random_state=random_state
    )
    return train, test
