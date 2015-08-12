# libs
    # absolute function
import math;

# functions
from matrixInit import unlabeledDistriMatrixInit;
from matrixInit import labeledDistriMatrixInit;
from matrixInit import stringIndexMatrixInit;
from matrixUpdate import featureWeightMatrixListUpdate;
from matrixUpdate import weightMatrixUpdate;
from matrixEntropyFun import matrixEntropyFun;
from harmonicFun import harmonicFun;
from AffinityFunMatrixListInit import AffinityFunSubMatrixInit;
from AffinityFunMatrixListInit import linearizeFun;
from AffinityFunMatrixListInit import AffinityFunMatrixListInit;

# constants
from constants import *;

# Input: 
# (a) [string list] the labeled node list
# (b) [string list] the unlabeled node list
# (c) [string] the current time stamp 
# (d) [dict] labeled : AQI
# (e) [int] the # of features of each node
# Output:
# [pandas DataFrame] the unlabeled distribution matrix Pu after 1 AQInf call

# haven't implemented:
# (a) labeledFeatureDictList
# (b) unlabeledFeatureDictList

def AQInf(labeledList,
          unlabeledList,
          timeStamp,
          labeledAQIDict,
          labeledFeatureDictListUponTimeStamp,
          unlabeledFeatureDictListUponTimeStamp,
          numOfFeatures):
    
    # initialize Pu
    unlabeledDistriMatrix = unlabeledDistriMatrixInit(unlabeledList, MAX_AQI + 1);
    
    # construct labeledDistriMatrix Pv from labeledAQIDict
    labeledDistriMatrix = labeledDistriMatrixInit(labeledAQIDict, MAX_AQI + 1);

    # construct the node list
    nodeList = labeledList + unlabeledList;
    
    # construct AffinityFunMatrix list from featureDict list
    AffinityFunMatrixList = AffinityFunMatrixListInit(nodeList,
                                                      labeledFeatureDictListUponTimeStamp[timeStamp],
                                                      unlabeledFeatureDictListUponTimeStamp[timeStamp],
                                                      numOfFeatures,
                                                      labeledAQIDict);

    # initialize feature weight matrix
    featureWeightMatrixList = [];

    for i in range(numOfFeatures):
        featureWeightMatrixList.append( stringIndexMatrixInit(nodeList, nodeList, 1.0) );

    # update weight matrix
    weightMatrix = weightMatrixUpdate(featureWeightMatrixList, AffinityFunMatrixList, numOfFeatures);

    # calculate old entropy H(Pu)
    lastUnlabeledDistriEntropy = matrixEntropyFun(unlabeledDistriMatrix);

    # assign the old entropy H(Pu) to diff(H(Pu)) and start iteration
    unlabeledDistriEntropyDiff = lastUnlabeledDistriEntropy;

    # iteration starts:
    while unlabeledDistriEntropyDiff > CONV_THRESHOLD:
    
        # update Pik matrix
        featureWeightMatrixListUpdate(featureWeightMatrixList,
                                      weightMatrix,
                                      AffinityFunMatrixList,
                                      numOfFeatures);

        # update weight matrix
        weightMatrix = weightMatrixUpdate(featureWeightMatrixList, AffinityFunMatrixList, numOfFeatures);

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
