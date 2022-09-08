import numpy as np
import pandas as pd


def get_bands_max(df):
    # TODOx

    # CONVERT PYSPARK ARRAY AS PANDAS ARRAY FOR EASY COMPUTATIONS
    pandasDF = df.toPandas()
    noOfBands = pandasDF['bands'][1]
    # EXTRACT ONLY ONE COLOUMN ON WHICH WE HAVE TO PERFORM OPERATIONS
    NPDataArray = pandasDF['data'].to_numpy()

    # THIS WILL BE THE OUTPUT ARRAY WHICH WILL BE CONVERTED TO NP ARRAY WHILE RETURNING
    outputArray = []

    # NPDATA ARRAY WILL HAVE EACH ELEMENT AS AN INDIVIDUAL IMAGE
    for everyImage in NPDataArray:

        # EACH IMAGE COMPRISES NO OF BANDS, SO WE WILL SPLIT THE IMAGE INTO 4 EQUAL PARTS
        splittedImage = np.array_split(everyImage, noOfBands)

        # EACH ELEMENTARRAY IS EACH BANDS OF AN IMAGE
        elementOfOutputArray = []

        # SO FOR EVERY BAND IN THE SPLITTED IMAGE WE WILL FIND THE MAX OF AN ARRAY AND APPEND IT
        for everyBand in splittedImage:
            elementOfOutputArray.append(everyBand.max())

        # SINCE WE WANT OUTPUT AS NUMBER OF IMAGE x NUMBER OF BANDS MATRIX
        # WE NEED TO ADD ALL FOUR VALUES'S ARRAY TO THE OUTPUT ARRAY AT THE LAST
        outputArray.append(elementOfOutputArray)

    # RETURN NUMPY ARRAY
    return np.asarray(outputArray)
