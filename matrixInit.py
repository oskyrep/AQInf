# Input: 
# (a) [string list] the unlabeled node list
# (b) [int] the maximum AQI value
# Output:
# [2D dict] the matrix whose entities share maxAQI values

import collections;

def matrixInit(nodeList, entity, isDistri):
    
    matrix = collections.OrderedDict();

    if isDistri == True:
        
        for node in nodeList:
            matrix[node] = [];
            for currentAQI in range(0, MAX_AQI+1, 1):
                matrix[node].append(entity);
    else:
        
        for nodeRowIndex in nodeList:
            matrix[nodeRowIndex] = collections.OrderedDict();
            for nodeColIndex in nodeList:
                matrix[nodeRowIndex][nodeColIndex] = entity;
    
    return matrix;
