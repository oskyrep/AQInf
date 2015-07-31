import pandas as pd;
import collections;

# Input: 
# (a) [string list] the unlabeled node list
# (b) [float] the entity default value to be filled in
# Output:
# [2D dict] the matrix whose entities share maxAQI values

def unlabeledDistriMatrixInit(unlabeledList, numOfClasses):
    
    return pd.DataFrame([ [1.0 / numOfClasses] * len(unlabeledList) ] * numOfClasses,
                        index = range(0, numOfClasses),
                        columns = unlabeledList,
                        dtype = float);

def labeledDistriMatrixInit(labeledAQIList, numOfClasses):

    distriMatrix = pd.DataFrame([ [0] * len(labeledAQIList.keys()) ] * numOfClasses,
                                index = range(0, numOfClasses),
                                columns = labeledAQIList.keys(),
                                dtype = float);

    for (labeledNode, AQI) in labeledAQIList.items():
        distriMatrix[labeledNode][AQI] = 1.0;

    return distriMatrix;

# Input: 
# (a) [string list] the row index node list
# (b) [string list] the col index node list
# (c) [float] the entity default value to be filled in
# Output:
# [2D dict] the matrix whose entities are (c)

def stringIndexMatrixInit(rowIndexList, colIndexList, entity):
        
    rowValue = collections.OrderedDict.fromkeys(colIndexList, entity);

    return collections.OrderedDict.fromkeys(rowIndexList, rowValue);


