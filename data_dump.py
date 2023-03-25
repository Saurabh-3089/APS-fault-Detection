import pymongo
import pandas as pd
import json
from sensor.config import mongo_client

FILE_PATH="/config/workspace/aps_failure_training_set1.csv"
DATABASE_NAME="aps"
COLLECTION_NAME="sensor"

if __name__=="__main__":
    df = pd.read_csv(FILE_PATH)
    print(f"Rows and Columns: {df.shape}")

    #convert df to json to dump csv to MongoDB
    #Drop the index
    df.reset_index(drop=True,inplace=True)

    #json.loads convert json to python dictionary object
    json_record=list(json.loads(df.T.to_json()).values())
    #print(json_record[0])

    #insert converted json record to mongo db
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
