from src.logger import logging
from src.exception import TrainException
import os, sys
from datetime import datetime
from src.entity.config_entity import ModelEvaluationConfig, ModelPusherConfig, ModelTrainerConfig, TrainingPipelineConfig, DataIngestionConfig
from src.constants.training_pipeline import *
from src.constants import TIMESTAMP
class RecommenderConfig:
    def __init__(self, pipeline_name = PIPELINE_NAME, timestamp = TIMESTAMP):
        self.timestamp = timestamp
        self.pipeline_name = pipeline_name
        self.pipeline_config = self.get_pipeline_config()

    def get_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            artifact_dir = ARTIFACT_DIR
            pipeline_config = TrainingPipelineConfig(pipeline_name=self.pipeline_name,
                                                     artifact_dir=artifact_dir)
            logging.info(f"Pipeline configuration: {pipeline_config}")
            return pipeline_config
        except Exception as e:
            raise TrainException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            """
            master directory for data ingestion
            we will store metadata information and ingested file to avoid redundant download
            """

            data_ingestion_master_dir = os.path.join(self.pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
        
            # time based directory for each run
            data_ingestion_dir = os.path.join(data_ingestion_master_dir,self.timestamp)

            data_ingestion_config = DataIngestionConfig(
                data_ingestion_dir=data_ingestion_dir,
                all_interactions_file_path=os.path.join(data_ingestion_dir,DATA_INGESTION_ALL_DATA_DIR),
                interactions_train_file_path=os.path.join(data_ingestion_dir,DATA_INGESTION_INTERACTIONS_TRAIN_FILE_NAME),
                interactions_test_file_path=os.path.join(data_ingestion_dir,DATA_INGESTION_INTERACTIONS_TEST_FILE_NAME),
                interactions_split_percentage=DATA_INGESTION_INTERACTIONS_SPLIT_PERCENTAGE
                )

            logging.info(f"Data ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise TrainException(e, sys)


    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            model_trainer_dir = os.path.join(self.pipeline_config.artifact_dir,
                                             MODEL_TRAINER_DIR_NAME, self.timestamp)
            trained_model_file_path = os.path.join(
                model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR)
            
            trained_model_name = os.path.join(
                trained_model_file_path,MODEL_TRAINER_TRAINED_INTERACTIONS_MODEL_NAME)

            model_matrix_name = os.path.join(
                model_trainer_dir, MODEL_TRAINER_INTERACTIONS_MATRIX_FILE_NAME)
            
            model_trainer_config = ModelTrainerConfig(model_trainer_dir=model_trainer_dir,
                                                      trained_interactions_model_file_path=trained_model_name,
                                                      interactions_matrix_file_path=model_matrix_name,)
                                                      
            logging.info(f"Model trainer config: {model_trainer_config}")
            return model_trainer_config
        except Exception as e:
            raise TrainException(e, sys)

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        try:
            model_evaluation_dir = os.path.join(self.pipeline_config.artifact_dir,MODEL_EVALUATION_DIR_NAME)

            model_evaluation_report_file_path = os.path.join(
                model_evaluation_dir, MODEL_EVALUATION_REPORT_NAME)
            
            model_evaluation_config = ModelEvaluationConfig(model_evaluation_dir=model_evaluation_dir,
                                                            report_file_path=model_evaluation_report_file_path,
                                                            change_threshold=MODEL_EVALUATION_CHANGED_HITRATE_THRESHOLD)
            
            logging.info(f"Model evaluation config: [{model_evaluation_config}]")
            return model_evaluation_config

        except Exception as e:
            raise TrainException(e, sys)

    def get_model_pusher_config(self) -> ModelPusherConfig:
        try:
            model_pusher_dir = os.path.join(self.pipeline_config.artifact_dir,MODEL_PUSHER_DIR_NAME)
            production_timestamp = self.timestamp
            self.saved_production_model_file_path = os.path.join(SAVED_MODEL_DIR,f"{production_timestamp}")
            model_pusher_config = ModelPusherConfig(
                model_pusher_dir=model_pusher_dir,
                best_interactions_model_file=os.path.join(model_pusher_dir,BEST_INTERACTIONS_MODEL_FILE_NAME),
                best_interactions_model_report_file=os.path.join(model_pusher_dir,BEST_INTERACTIONS_MODEL_REPORT_FILE_NAME),
                best_interactions_model_matrix_file=os.path.join(model_pusher_dir,BEST_INTERACTIONS_MODEL_MATRIX_FILE_NAME),
                saved_production_model_file_path=os.path.join(self.saved_production_model_file_path,PRODUCTION_INTERACTIONS_MODEL_FILE_NAME),
                saved_production_interactions_model_file=os.path.join(self.saved_production_model_file_path,PRODUCTION_INTERACTIONS_MODEL_FILE_NAME),
                saved_production_interactions_model_report_file=os.path.join(self.saved_production_model_file_path,PRODUCTION_INTERACTIONS_MODEL_REPORT_FILE_NAME),
                saved_production_interactions_matrix_file=os.path.join(self.saved_production_model_file_path,PRODUCTION_INTERACTIONS_MATRIX_FILE_NAME)
            )
            logging.info(f"Model pusher config: {model_pusher_config}")
            return model_pusher_config
        except  Exception as e:
            raise TrainException(e, sys)









    