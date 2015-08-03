import math;

def featureWeightMatrixListUpdate(featureWeightMatrixList, weightMatrix, AffinityFunMatrixList):
    
    for i in range( len(featureWeightMatrixList) ):
        featureWeightMatrixList[i] = (1.0 - 2.0 * weightMatrix * \
                                      AffinityFunMatrixList[i]) * \
                                      featureWeightMatrixList[i];

def weightMatrixUpdate(featureWeightMatrixList, AffinityFunMatrixList):

    tempMatrixList = [0.0] * len(featureWeightMatrixList);
    
    for i in range( len(featureWeightMatrixList) ):
        tempMatrixList[i] = featureWeightMatrixList[i] * \
                            featureWeightMatrixList[i] * \
                            AffinityFunMatrixList[i];

    tempWeightMatrix = - sum(tempMatrixList);
    
    return tempWeightMatrix.applymap(math.exp);
