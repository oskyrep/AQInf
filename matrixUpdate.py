# libs
import math;

# Input:
# (a) [list of pandas DataFrame] the list of feature weight matrix
# (b) [pandas DataFrame] the weight matrix
# (c) [list of pandas DataFrame] the list of Affinity Function matrix
# Output:
# None, the operation is done on (a)

def featureWeightMatrixListUpdate(featureWeightMatrixList,
                                  weightMatrix,
                                  AffinityFunMatrixList,
                                  numOfFeatures):
    
    for i in range( numOfFeatures ):
        featureWeightMatrixList[i] = (1.0 - 2.0 * weightMatrix * \
                                      AffinityFunMatrixList[i]) * \
                                     featureWeightMatrixList[i];

# Input:
# (a) [list of pandas DataFrame] the list of feature weight matrix
# (b) [list of pandas DataFrame] the list of Affinity Function matrix
# Output:
# [pandas DataFrame] the updated weight matrix

def weightMatrixUpdate(featureWeightMatrixList, AffinityFunMatrixList, numOfFeatures):

    tempMatrixList = [0.0] * numOfFeatures;
    
    for i in range( numOfFeatures ):
        tempMatrixList[i] = featureWeightMatrixList[i] * \
                            featureWeightMatrixList[i] * \
                            AffinityFunMatrixList[i];

    tempWeightMatrix = - sum(tempMatrixList);
    
    return tempWeightMatrix.applymap(math.exp);
