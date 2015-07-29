import collections;
from twoDimDictListTransformation import twoDimListToTwoDimDict;

# Input: 
# (a) [string list] the unlabeled node list
# (b) [float] the entity default value to be filled in
# Output:
# [2D dict] the matrix whose entities share maxAQI values

def distriMatrixInit(rowIndexList, entity):
    
    numOfRows = len(rowIndexList);
    tempTwoDimList = [ [entity] * (MAX_AQI+1) ] * numOfRows;

    return twoDimListToTwoDimDict(tempTwoDimList, rowIndexList);

# Input: 
# (a) [string list] the row index node list
# (b) [string list] the col index node list
# (c) [float] the entity default value to be filled in
# Output:
# [2D dict] the matrix whose entities are (c)

def stringIndexMatrixInit(rowIndexList, colIndexList, entity):
        
    matrix = collections.OrderedDict();

    for rowIndex in rowIndexList:
        matrix[rowIndex] = collections.OrderedDict();
        for colIndex in colIndexList:
            matrix[rowIndex][colIndex] = entity;

    return matrix;
