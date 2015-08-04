# libs
import pandas as pd;
import numpy as np;
    # log fun
import math;

# Input:
# [float] numpy matrix's entity
# Output:
# [float] new numpy matrix's entity after operation

def entropyFun(entity):
    
    if entity == 0.0 or entity == 1.0:
        return 0.0;
    else:
        return entity * math.log(entity, 2) + (1-entity) * math.log(1-entity, 2);

# Input:
# [pandas DataFrame] the matrix whose entropy to be calculated
# Output:
# [float] the matrix entropy after calculation

def matrixEntropyFun(dataFrame):
    
    # transform the pandas dataFrame into numpy array
    matrix = dataFrame.T.values;

    # the # of nodes = the first dim of matrix
    numOfNodes = matrix.shape[0];
    
    # apply the matrix opeartion function to entropyFun
    entityEntropyFun = np.vectorize(entropyFun, otypes=[np.float]);

    return - ( np.sum( entityEntropyFun(matrix) ) ) / numOfNodes;
