# matrix manipulation
import numpy as np;
# inverse matrix
from numpy.linalg import inv;
# dict list tranformation
from twoDimDictListTransformation import twoDimDictToTwoDimList;
from twoDimDictListTransformation import twoDimListToTwoDimDict;

# Input:
# [2D dict] the weight matrix
# Output:
# [2D dict] the labeled distribution matrix

def harmonicFun(weightMatrixRHS, labeledDistriMatrixRHS, unlabeledList):
    
    weightMatrix = np.array( twoDimDictToTwoDimList(weightMatrixRHS) );
    labeledDistriMatrix = np.array( twoDimDictToTwoDimList(labeledDistriMatrixRHS) );

    # l: the # of labeled points
    l = labeledDistriMatrix.shape[0];

    # n: the total # of points
    n = weightMatrix.shape[0];

    # the graph Laplacian L = D - W
    LaplacianMatrix = np.diag( np.sum(weightMatrix, axis=1) );
    LaplacianMatrix = np.subtract(LaplacianMatrix, weightMatrix);
    
    # the harmonic function
    unlabeledDistriMatrix = - inv( LaplacianMatrix[l:n:1, l:n:1] )
                      * LaplacianMatrix[l:n:1, 0:l:1]
                      * labeledDistriMatrix;

    return twoDimListToTwoDimDict( unlabeledDistriMatrix.tolist(), unlabeledList );
