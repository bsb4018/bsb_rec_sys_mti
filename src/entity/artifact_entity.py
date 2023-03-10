from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataIngestionArtifact:
    trained_interactions_file_path: str
    test_interactions_file_path: str
    interactions_all_data_file_path: str
    users_all_data_file_path: str
    

@dataclass
class ModelTrainerArtifact:
    trained_interactions_model_file_path: str
    interactions_matrix_shape_file_path: str
    users_id_map_file_path: str
    users_feature_map_file_path: str
    #all_data_train_model_file_path: str

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_hitrate: float
    best_model_path: str
    best_model_report_path: str
    current_interactions_model_path: str
    interactions_matrix_shape_file_path: str
    current_interactions_model_report_file_path: str
    users_id_map_file_path: str
    users_feature_map_file_path: str
    
@dataclass
class ModelPusherArtifact:
    model_file_path:str
    #best_interactions_model_file:str
    saved_best_interactions_model_file:str
    saved_interactions_matrix_shape_file_path:str
    saved_users_id_map_file_path:str
    saved_users_feature_map_file_path:str

    