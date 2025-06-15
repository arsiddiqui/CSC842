#Developer: Ashar Siddiqui
#Date Created: 06/15/2025
#Date Updated: 06/15/2025
#Email Scanner - dbUtility.py
#Change Log

#CSC 842, Security tool development Cycle 5

import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def loadConfig(path="config.json"):
   with open(path, "r") as f:
        return json.load(f)


def getMongoClient(config):
    uri = config["mongo_uri"]
    userName = config.get("userId")
    password = config.get("password")
    client = MongoClient(uri, username=userName, password=password)
    return client


def getTraingData(configPath="config.json"):

    config = loadConfig(configPath)
    client = getMongoClient(config)
 
    col = client[config["mongo_db"]][config["mongo_collection"]]

    cursor = col.find({})

    texts, labels = [],[]
    
    for doc in cursor:
        texts.append(doc.get("text", ""))
        labels.append(doc.get("label", 0))
    return texts, labels

def testGetMongoClient(configPath="config.json"):
    
    try:
        config = loadConfig(configPath)
        client = getMongoClient(config)
       
        print("Connected to Mongo...")

        col = client[config["mongo_db"]][config["mongo_collection"]]
     
        for doc in col.find({}).limit(5):
            print(doc)

    except ConnectionFailure:
        print("Failed to connect...")
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    testGetMongoClient()
