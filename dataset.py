
import pandas as pd
import os
from config import Config
from typing import Tuple
from type_aliases import Path
from type_aliases import RangesDataset, EmosVectorsDataset, SynthDataset, Dataset
from sklearn.model_selection import train_test_split
from source_code_utils import complement_range_file


def get_emos_ranges(path_to_csv: Path) -> RangesDataset:
    ''' Load and prepare dataset with calculated possible EMO ranges '''
    emos_ranges = pd \
        .read_csv(path_to_csv, header=None, names=['filename', 'class_name', 'method_name', 'ranges']) \
        .drop_duplicates(['filename'], keep=False)
    emos_ranges.filename = emos_ranges.filename.apply(os.path.basename)
    return emos_ranges


def get_emos_vectors(path_to_csv: Path) -> EmosVectorsDataset:
    ''' Load and prepare dataset with EMOs and corresponding vectors'''
    def _mk_link_to_original_sample(filename) -> str:
        return '_'.join(filename.split('_')[0: 4]) + '.java'

    def _ex_range(filename) -> str:
        out = list(map(int, filename.replace('.java', '').split('_')[-2:]))
        return str(out)

    emos_vectors = pd \
        .read_csv(path_to_csv, header=None, names=['emo_uid', 'vector_str']) \
        .drop_duplicates(['emo_uid'], keep=False)
    emos_vectors.emo_uid = emos_vectors.emo_uid.apply(os.path.basename)
    emos_vectors['filename_origin'] = emos_vectors.emo_uid.apply(_mk_link_to_original_sample)
    emos_vectors['range'] = emos_vectors.emo_uid.apply(_ex_range)
    return emos_vectors


def _figure_out_true_inline_range(row: pd.core.series.Series) -> str:
    start = int(row['insertion_start']) - 1
    end = int(row['insertion_end']) - 1
    if end < start:
        return None
    range = complement_range_file(
        row['output_filename'],
        start,
        end,
    )
    return str(range)


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

    df = pd.read_csv(path_to_dataset_csv).drop_duplicates(['output_filename'], keep=False)[columns]
    df['filename'] = df.output_filename.apply(os.path.basename)
    df['output_filename'] = df.output_filename.apply(lambda v: f'{path_to_java_files}/{v}')
    df['true_inline_range'] = df.apply(lambda row: _figure_out_true_inline_range(row), axis=1)
    df.dropna(subset=['true_inline_range'], inplace=True)  # drop rows where True EMO is undefined
    return df


def combine_all_together(emos: EmosVectorsDataset, synth: SynthDataset) -> Dataset:
    pass


def get_dataset(config: Config) -> pd.DataFrame:
    '''Load, preprocess and combine all input data parts together to form a single dataset'''
    synth = get_synth_dataset(config.path_to_dataset_csv, config.path_to_java_files)
    print("Synth dataset:", len(synth))
    emos_ranges = get_emos_ranges(config.path_to_ranges_csv)
    print("Ranges dataset:", len(emos_ranges))
    emos_vectors = get_emos_vectors(config.path_to_emos_vectors)
    print("EMOS vectors dataset:", len(emos_vectors))
    ds = combine_all_together(emos_ranges, emos_vectors, synth)
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
