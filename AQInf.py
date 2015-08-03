# absolute function
import math;
from matrixInit import unlabeledDistriMatrixInit;
from matrixInit import labeledDistriMatrixInit;
from matrixInit import stringIndexMatrixInit;
from matrixUpdate import featureWeightMatrixListUpdate;
from matrixUpdate import weightMatrixUpdate;
from matrixEntropyFun import matrixEntropyFun;
from harmonicFun import harmonicFun;

# constants

# Input: 
# (a) [string list] a set of locations V with existing measurement stations;
# (b) [string list] a set of query locations U without stations;
# (c) [string list] the time interval ti of interest;
# (d) [1D dict] the labeled nodes with their AQI values;
# Output:
# [2D dict] the unlabeled AQI distribution Pu;

def AQInf(labeledList, unlabeledList, timeStampList, labeledAQIDict):
    
    # initialize Pu
    unlabeledDistriMatrix = unlabeledDistriMatrixInit(unlabeledList, MAX_AQI + 1);
    
    # construct labeledDistriMatrix from labeledAQIDict
    labeledDistriMatrix = labeledDistriMatrixInit(labeledAQIDict, MAX_AQI + 1);

    # construct the node list
    nodeList = labeledList + unlabeledList;
    
    # construct AG based on the node list
    # construct the whole stuff

    # initsialize feature weight matrix
    featureWeightMatrixList = [];

    for i in range(numOfFeatures):
        featureWeightMatrixList.append(stringIndexMatrixInit(nodeList, nodeList, 1.0));

    # update weight matrix
    weightMatrix = weightMatrixUpdate(featureWeightMatrixList, AffinityFunMatrixList);

    # calculate old entropy H(Pu)
    lastUnlabeledDistriEntropy = matrixEntropyFun(unlabeledDistriMatrix);

    # assign the old entropy H(Pu) to diff(H(Pu)) and start iteration
    unlabeledDistriEntropyDiff = lastUnlabeledDistriEntropy;

    # iteration starts:
    while unlabeledDistriEntropyDiff > CONV_THRESHOLD:
    
        # update Pik matrix
        featureWeightMatrixListUpdate(featureWeightMatrixList, weightMatrix, AffinityFunMatrixList);

        # update weight matrix
        weightMatrix = weightMatrixUpdate(featureWeightMatrixList, AffinityFunMatrixList);

        # update Pu through harmonic function
        unlabeledDistriMatrix = harmonicFun(weightMatrix,
                                            labeledDistriMatrix,
                                            list(unlabeledDistriMatrix.columns));
        
        # compute entropy of unlabeled distribution matrix
        unlabeledDistriEntropy = matrixEntropyFun(unlabeledDistriMatrix);

        # update the loop conditional statement
        unlabeledDistriEntropyDiff = math.fabs(unlabeledDistriEntropy - lastUnlabeledDistriEntropy);
        lastUnlabeledDistriEntropy = unlabeledDistriEntropy;

    return unlabeledDistriMatrix;
