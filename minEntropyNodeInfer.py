import pandas as pd;
from collections import OrderedDict;
from matrixEntropyFun import f;
from matrixEntropyFun import matrixEntropyFun;

# Input:
# [2D dict of float values] the distribution matrix to be inferred
# Output:
# [string] the node with the smallest entropy

def minEntropyNodeInfer(distriMatrix):
    
    nodeEntropyList = OrderedDict();

    for node in distriMatrix.keys():
        # the matrixEntropyFun's input has to be 2D dict
        # transform a row in distriMatrix into 2D dict
        nodeEntropyList[node] = matrixEntropyFun( distriMatrix.ix[ : , node : node] );
            
    # return the node with the smallest entropy
    return min(nodeEntropyList, key = nodeEntropyList.get);
