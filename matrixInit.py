#!/usr/bin/python

# libs
import pandas as pd;
import collections;

# Input: 
# (a) [string list] the unlabeled node list
# (b) [float] the # of AQI classes
# Output:
# [pandas DataFrame] the unlabeled distribution matrix Pu after initialization

def unlabeledDistriMatrixInit(unlabeledList, numOfClasses):
    
    return pd.DataFrame([ [1.0 / numOfClasses] * len(unlabeledList) ] * numOfClasses,
                        index = range(numOfClasses),
                        columns = unlabeledList,
                        dtype = float);

# Input: 
# (a) [dict] labeled : AQI
# (b) [float] the # of AQI classes
# Output:
# [pandas DataFrame] the labeled distribution matrix Pv after initialization

def labeledDistriMatrixInit(labeledAQIDict, numOfClasses):

    distriMatrix = pd.DataFrame([ [0] * len(labeledAQIDict.keys()) ] * numOfClasses,
                                index = range(numOfClasses),
                                columns = labeledAQIDict.keys(),
                                dtype = float);

    for (labeledNode, AQI) in labeledAQIDict.items():
        distriMatrix[labeledNode][AQI] = 1.0;

    return distriMatrix;

# Input: 
# (a) [string list] the row index node list
# (b) [string list] the col index node list
# (c) [float] the entity default value to be filled in
# Output:
# [pandas DataFrame] the matrix whose entities are (c)

def stringIndexMatrixInit(rowIndexList, colIndexList, entity):
        
    return pd.DataFrame([ [entity] * len(colIndexList) ] * len(rowIndexList),
                        index = rowIndexList,
                        columns = colIndexList,
                        dtype = float);
