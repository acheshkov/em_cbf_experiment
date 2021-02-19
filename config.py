from dataclasses import dataclass

@dataclass
class Config:
    path_to_range: str
    path_to_emos_vectors: str
    path_to_dataset: str
    path_to_java_files: str
    path_to_semi_jar: str