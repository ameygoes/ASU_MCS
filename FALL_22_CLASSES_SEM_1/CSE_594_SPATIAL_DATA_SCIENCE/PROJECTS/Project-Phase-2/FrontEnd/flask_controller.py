import requests
import pandas as pd
import json
import json

import pandas as pd
import requests


# UTILITY FUNCTION TO MODIFY DATASET FROM THE GIVEN PATH - FROM UPLOADS FOLDER
# THE FUNCTION WRITES DATA.JSON FILE TO INTERMEDIATE FOLDER WHICH IS USED BY
# TRIPS LAYER TO VISUALIZE RESULTS
# def load_dataset(path):
#     df = pd.read_json(path)
#     df["locs"] = df["trajectory"].apply(lambda f: [item["location"][::-1] for item in f])
#     df["times"] = df["trajectory"].apply(lambda f: [item["timestamp"] - 1664511371 for item in f])
#     df.drop(["trajectory"], axis=1, inplace=True)
#     return updateDFMap(df)

def load_dataset(path):
    df = pd.read_json(path)
    mintime = df["trajectory"][0][0]["timestamp"]
    for tj in df["trajectory"]:
        for data in tj:
            mintime = min(mintime, data["timestamp"])
    df["locs"] = df["trajectory"].apply(lambda f: [item["location"][::-1] for item in f])
    df["times"] = df["trajectory"].apply(lambda f: [item["timestamp"] - mintime for item in f])
    df.drop(["trajectory"], axis=1, inplace=True)
    return updateDFMap(df)

# THIS FUNCTION MAKES A POST CALL TO GET SPATIAL RANGE DATAFRAME TO SCALA BACKEND
# WRITES THE OUTPUT TO INTERMEDIATE FOLDER TO OVERWRITE THE DATA.JSON FILE
# WHICH IS USED TO VISUALIZE THE OUTPUT IN TRIPS LAYER
def getGSRDataFrame(gsrURL, latMin, lonMin, latMax, lonMax):
    srJsonResponse = requests.post(gsrURL,
                                   json={"latMin": latMin, "lonMin": lonMin, "latMax": latMax, "lonMax": lonMax})

    return getCleanedDF(srJsonResponse)


# THIS FUNCTION MAKES A POST CALL TO GET SPATIAL TEMPORAL RANGE DATAFRAME TO SCALA BACKEND
# WRITES THE OUTPUT TO INTERMEDIATE FOLDER TO OVERWRITE THE DATA.JSON FILE
# WHICH IS USED TO VISUALIZE THE OUTPUT IN TRIPS LAYER
def getGSTRDataFrame(gstrURL, timemin, timeMax, latMin, lonMin, latMax, lonMax):
    srJsonResponse = requests.post(gstrURL,
                                   json={"timeMin": timemin, "timeMax": timeMax, "latMin": latMin, "lonMin": lonMin,
                                         "latMax": latMax, "lonMax": lonMax})

    return getCleanedDF(srJsonResponse)


# THIS FUNCTION MAKES A POST CALL TO GET SPATIAL TEMPORAL RANGE DATAFRAME TO SCALA BACKEND
def getKNNDataFrame(gKnnURL, trajectoryId, k):
    srJsonResponse = requests.post(gKnnURL, json={"trajectoryId": trajectoryId, "neighbors": k})
    return getCleanedDF(srJsonResponse)[0]


# THIS FUNCTION IS DEPRECATED AND IS NOT IN USE CURRENTLY
def getLoadedDataFrame(loadURL, path):
    srJsonResponse = requests.post(loadURL, json={"path": path})
    return getCleanedDF(srJsonResponse)[0]


# THIS FUNCTION IS USED TO SEND A STRING RESPONSE IF THE GLOBAL VARIABLE
# FILE PATH IS UPDATED OR NOT
def getLoadedDataFrame2(loadURL, path):
    srJsonResponse = requests.post(loadURL, json={"path": path})
    return srJsonResponse


# THIS FUNCTION RETURNS A VIEW STATE WHICH IS USED BY TRIPS LAYER AS A START POINT
# AKA VIEW POINT / STATE
def getViewState(df):
    print(type(df))
    return {'latitude': df[0]["locs"][0][0], 'longitude': df[0]["locs"][0][1], 'zoom': 11, 'bearing': 0, 'pitch': 45}


# THIS FUNCTION IS A UTILITY FUNCTION WHICH CHECKS IF THE FILE IS IN CORRECT FORMAT OR NOT
def allowed_file(filename):
    if filename.split(".")[1] != 'json':
        return False
    return True


# THIS FUNCTION RETURNS A CLEANED DF
# WHICH IS JSON STRING WITH BACKSLASH REPLACED
# IT THEN CREATES A DATAFRAME OUT OF THAT STRING A RETURNS IT
def getCleanedDF(jsonResponse):
    textJsonResponse = eval(jsonResponse.text)
    temp = json.loads(str(textJsonResponse).replace("\'", ""))
    return pd.DataFrame(temp), temp


# THIS FUNCTION UPDATES DFMAP USED IN load_dataset() FUNCTION
def updateDFMap(df):
    dfMap = []
    for i in range(len(df["locs"])):
        dfMap.append({"locs": df["locs"][i], "times": df["times"][i], "trajectoryId": i})
    return dfMap


# THIS FUNCTION UPDATES JSON DATA USED IN spatialTemporalRange() and spatialRange()FUNCTION
# def updateJson(jsonData):
#     for elem in jsonData:
#         elem["times"] = elem["timestamp"]
#         elem["locs"] = []
#         for loc in elem["location"]:
#             elem["locs"].append(loc[::-1])
#         del elem["timestamp"]
#         del elem["location"]
#     return jsonData
def updateJson(jsonData):
    mintime = min(jsonData[0]["timestamp"])
    for elem in jsonData:
        mintime  = min(elem["timestamp"])
    for elem in jsonData:
        elem["times"] = elem["timestamp"]
        elem["times"] = [x - mintime for x in elem["times"]]
        elem["locs"] = []
        for loc in elem["location"]:
            elem["locs"].append(loc[::-1])
        del elem["timestamp"]
        del elem["location"]
    return jsonData

# THIS FUNCTION WRITES JSON DATA TO PATH GIVEN IN THE PARAMETER
def writeToFile(jsonData, path):
    jsonFile = json.dumps(jsonData)
    with open(path, "w") as outfile:
        outfile.write(jsonFile)
