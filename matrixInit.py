#!/usr/bin/python

# libs
import pandas as pd
import collections

def unlabeledDistriMatrixInit(unlabeledList, numOfClasses):
    
    return pd.DataFrame([ [1.0 / numOfClasses] * len(unlabeledList) ] * numOfClasses,
                        index = range(numOfClasses),
                        columns = unlabeledList,
                        dtype = float)

def labeledDistriMatrixInit(labeledAQIDict, numOfClasses):

    distriMatrix = pd.DataFrame([ [0] * len(labeledAQIDict.keys()) ] * numOfClasses,
                                index = range(numOfClasses),
                                columns = labeledAQIDict.keys(),
                                dtype = float)

    for (labeledNode, AQI) in labeledAQIDict.items():
        distriMatrix[labeledNode][AQI] = 1.0

    return distriMatrix

def stringIndexMatrixInit(rowIndexList, colIndexList, entity):
        
    return pd.DataFrame([ [entity] * len(colIndexList) ] * len(rowIndexList),
                        index = rowIndexList,
                        columns = colIndexList,
                        dtype = float)
