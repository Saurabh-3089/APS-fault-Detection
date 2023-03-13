import pandas as pd
import numpy as np
from sensor.entity import artifact_entity,config_entity
from sensor.logger import logging
from sensor.exception import SensorException
from typing import Optional
from sensor import utils
import os,sys
from xgboost import XGBClassifier
from sklearn.metrics import f1_score

class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)               
    
    def train_model(self,x,y):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_trainer(self,)-> artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading Train and Test Array")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Splitting input and target feature from both Train and Test Array")
            x_train, y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test, y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Training the model")
            model = self.train_model(x=x_train,y=y_train)
            
            logging.info(f"Calculating the F1 Train score")
            yhat_train = model.predict(x_train)
            f1_train_score = f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"Calculating the F1 Test score")
            yhat_test = model.predict(x_test)
            f1_test_score = f1_score(y_true=y_test, y_pred=yhat_test)

            logging.info(f"Train score: {f1_train_score} and Test Score: {f1_test_score}")

            logging.info(f"Checking for under-fitting")
            #check for over-fitting or under-fitting or expected score
            if f1_test_score<self.model_trainer_config.expected_score:
                logging.info("Under-fitting Detected")
                raise Exception(f"Model is not good as not able to give good accuracy: {self.model_trainer_config.expected_score}: Model actual score : {f1_test_score}")
            
            logging.info(f"Checking for over-fitting")
            difference = abs(f1_train_score-f1_test_score)
            if difference>self.model_trainer_config.overfitting_thres:
                logging.info("Over-fitting Detected")
                raise Exception(f"Training and Testing Score difference: {difference} is more than Over-fitting Threshold: {self.model_trainer_config.overfitting_thres}")
            
            logging.info(f"Saving the Trained Model")
            #Save the trained Model
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            logging.info(f"Preparing the Artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, f1_train_score=f1_train_score,
                                                    f1_test_score=f1_test_score)
            logging.info(f"Model Trainer Artifact: {model_trainer_artifact} ")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys) 