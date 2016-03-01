#!/usr/bin/python

# libs
import pandas as pd
import numpy as np
    # log fun
import math

def entropyFun(entity):
    
    if entity == 0.0 or entity == 1.0:
        return 0.0
    else:
        return entity * math.log(entity, 2) + (1-entity) * math.log(1-entity, 2)

def matrixEntropyFun(dataFrame):
    
    # transform the pandas dataFrame into numpy array
    matrix = dataFrame.T.values

    # the # of nodes = the first dim of matrix
    numOfNodes = matrix.shape[0]
    
    # apply the matrix opeartion function to entropyFun
    entityEntropyFun = np.vectorize(entropyFun, otypes=[np.float])

    return - ( np.sum( entityEntropyFun(matrix) ) ) / numOfNodes
