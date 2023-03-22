from sensor.exception import SensorException
from sensor.logger import logging
from sensor.predictor import ModelResolver
from sensor.utils import load_object
from datetime import datetime
import pandas as pd
import numpy as np
import os,sys
PREDICTION_DIR = "prediction"

def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info(f"Creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading file: {input_file_path}")
        df = pd.read_csv(input_file_path)
        df.replace({"na":np.NAN},inplace=True)

        logging.info("Loading Transformer to transform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
        input_feature_names = list(transformer.feature_names_in_)
        input_arr = transformer.transform(df[input_feature_names])

        logging.info("Loading Model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)

        logging.info("Loading Target Encoder to convert numeric to categorical values")
        target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())
        car_prediction = target_encoder.inverse_transform(prediction)

        df["prediction"] = prediction
        df["cate_pred"] = car_prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)

        return prediction_file_path
    except Exception as e:
        raise SensorException(e, sys)


