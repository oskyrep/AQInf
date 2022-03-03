# libs
import pandas as pd
from collections import OrderedDict

# functions
from matrixEntropyFun import entropyFun
from matrixEntropyFun import matrixEntropyFun
import numpy as np

def minEntropyNodeInfer(distriMatrix):
    
    nodeEntropyDict = OrderedDict()

    for node in distriMatrix.keys():
        # the matrixEntropyFun's input has to be 2D dict
        # transform a row in distriMatrix into 2D dict
        nodeEntropyDict[node] = matrixEntropyFun( distriMatrix.ix[ : , node : node] )
            
    # return the node with the smallest entropy
    minEntropyNode = min(nodeEntropyDict, key = nodeEntropyDict.get)
    minEntropyNodeAQI = np.average(distriMatrix[minEntropyNode].index.values, weights = distriMatrix[minEntropyNode])
    return (minEntropyNode, minEntropyNodeAQI) #distriMatrix[minEntropyNode].argmax())
