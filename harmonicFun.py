#!/usr/bin/python

# libs
import numpy as np;
import pandas as pd;
    # inverse matrix
from numpy.linalg import inv;

# Input:
# (a) [pandas DataFrame] the weight matrix
# (b) [pandas DataFrame] the labeled distribution matrix Pv
# (c) [string list] the unlabeled node list
# Output:
# [pandas DataFrame] the unlabeled distribution matrix Pu after calculation

def harmonicFun(weightMatrixRHS, labeledDistriMatrixRHS, unlabeledList):
    
    weightMatrix = np.array( weightMatrixRHS.T.values );
    labeledDistriMatrix = np.array( labeledDistriMatrixRHS.T.values );

    # l: the # of labeled points
    l = labeledDistriMatrix.shape[0];

    # n: the total # of points
    n = weightMatrix.shape[0];

    # the graph Laplacian L = D - W
    LaplacianMatrix = np.diag( np.sum(weightMatrix, axis = 1) );
    LaplacianMatrix = np.subtract(LaplacianMatrix, weightMatrix);
    
    # the harmonic function
    unlabeledDistriMatrix = -1 * np.dot( np.dot( inv( LaplacianMatrix[l:n:1, l:n:1] ),
                                                 LaplacianMatrix[l:n:1, 0:l:1] ),
                                         labeledDistriMatrix );

    return pd.DataFrame(unlabeledDistriMatrix.transpose(),
                        index = range(unlabeledDistriMatrix.shape[1]),
                        columns = unlabeledList,
                        dtype = float);
