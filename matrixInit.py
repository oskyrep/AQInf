import collections;
from twoDimDictListTransformation import twoDimListToTwoDimDict;

# Input: 
# (a) [string list] the unlabeled node list
# (b) [float] the entity default value to be filled in
# Output:
# [2D dict] the matrix whose entities share maxAQI values

def distriMatrixInit(rowIndexList, numOfClasses):
    
    numOfRows = len(rowIndexList);
    entity = 1.0 / numOfClasses;

    tempTwoDimList = [ [entity] * numOfClasses ] * numOfRows;

    return twoDimListToTwoDimDict(tempTwoDimList, rowIndexList);

# Input: 
# (a) [string list] the row index node list
# (b) [string list] the col index node list
# (c) [float] the entity default value to be filled in
# Output:
# [2D dict] the matrix whose entities are (c)

def stringIndexMatrixInit(rowIndexList, colIndexList, entity):
        
    rowValue = collections.OrderedDict.fromkeys(colIndexList, entity);

    return collections.OrderedDict.fromkeys(rowIndexList, rowValue);

def labeledDistriMatrixInit(labeledAQIList, numOfClasses):

    distriMatrix = collections.OrderedDict.fromkeys(labeledAQIList.keys(), [0.0] * numOfClasses);

    for labeledNode in distriMatrix:
        distriMatrix[labeledNode][labeledAQIList[labeledNode]] = 1.0;

    return distriMatrix;
