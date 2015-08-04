# libs
import pandas as pd;
from collections import OrderedDict;

# functions
from matrixEntropyFun import entropyFun;
from matrixEntropyFun import matrixEntropyFun;

# Input:
# [pandas DataFrame] the distribution matrix to be inferred
# Output:
# (a) [string] the node with the smallest entropy
# (b) [int] the node's inferred AQI value

def minEntropyNodeInfer(distriMatrix):
    
    nodeEntropyDict = OrderedDict();

    for node in distriMatrix.keys():
        # the matrixEntropyFun's input has to be 2D dict
        # transform a row in distriMatrix into 2D dict
        nodeEntropyDict[node] = matrixEntropyFun( distriMatrix.ix[ : , node : node] );
            
    # return the node with the smallest entropy
    minEntropyNode = min(nodeEntropyDict, key = nodeEntropyDict.get);

    return (minEntropyNode, distriMatrix[minEntropyNode].argmax());
