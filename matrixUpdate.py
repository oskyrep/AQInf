# libs
import math;

# Input:
# (a) [list of pandas DataFrame] the list of feature weight matrix
# (b) [pandas DataFrame] the weight matrix
# (c) [list of pandas DataFrame] the list of Affinity Function matrix
# Output:
# None, the operation is done on (a)

def featureWeightMatrixListUpdate(featureWeightMatrixList, weightMatrix, AffinityFunMatrixList):
    
    for i in range( len(featureWeightMatrixList) ):
        featureWeightMatrixList[i] = (1.0 - 2.0 * weightMatrix * \
                                      AffinityFunMatrixList[i]) * \
                                      featureWeightMatrixList[i];

# Input:
# (a) [list of pandas DataFrame] the list of feature weight matrix
# (b) [list of pandas DataFrame] the list of Affinity Function matrix
# Output:
# [pandas DataFrame] the updated weight matrix

def weightMatrixUpdate(featureWeightMatrixList, AffinityFunMatrixList):

    tempMatrixList = [0.0] * len(featureWeightMatrixList);
    
    for i in range( len(featureWeightMatrixList) ):
        tempMatrixList[i] = featureWeightMatrixList[i] * \
                            featureWeightMatrixList[i] * \
                            AffinityFunMatrixList[i];

    tempWeightMatrix = - sum(tempMatrixList);
    
    return tempWeightMatrix.applymap(math.exp);
