import os,sys
from sensor.exception import SensorException
from sensor.logger import logging
from datetime import datetime

FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:

    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), "artifact", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise SensorException(e,sys)


class DataIngestionConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:    
            self.database_name="aps"
            self.collection_name="sensor"
            self.data_ingestion_dir= os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir, "feature_store",FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir, "dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir, "dataset",TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception  as e:
            raise SensorException(e,sys) 

    def to_dict(self)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e,sys)

        

class DataValidationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:    
            self.data_validation_dir= os.path.join(training_pipeline_config.artifact_dir,"data_validation")
            self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")  
            self.missing_threshold = 0.7    
            self.base_file_path=os.path.join("aps_failure_training_set1.csv")      
        except Exception  as e:
            raise SensorException(e,sys) 


class DataTransformationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_tranformation")
            self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
            self.transformed_train_path = os.path.join(self.data_transformation_dir,"transformer",TRAIN_FILE_NAME.replace("csv","npz"))
            self.transformed_test_path = os.path.join(self.data_transformation_dir,"transformer",TEST_FILE_NAME.replace("csv","npz"))
            self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)



class ModelTrainerConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir)
            self.model_path = os.path.join(self.model_trainer_dir, "model", MODEL_FILE_NAME)           
            self.expected_score = 0.7
            self.overfitting_thres = 0.1
        except Exception as e:
            raise SensorException(e, sys)

class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.change_threshold = 0.1
        except Exception as e:
            raise SensorException(e, sys)

class ModelPusherConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir,"Model Pusher")
            self.saved_model_dir = os.path.join("saved_models")
            self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
            self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
            self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORMER_OBJECT_FILE_NAME)
            self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)
