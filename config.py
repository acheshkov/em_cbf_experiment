from dataclasses import dataclass

@dataclass
class Config:
    path_to_range_csv: str
    path_to_emos_vectors_csv: str
    path_to_dataset_csv: str
    path_to_java_files: str
    path_to_semi_jar: str