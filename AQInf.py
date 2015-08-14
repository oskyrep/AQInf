# libs
import pandas as pd;
from collections import OrderedDict;
    # absolute function
import math;

# functions
from matrixInit import unlabeledDistriMatrixInit;
from matrixInit import labeledDistriMatrixInit;
from matrixInit import stringIndexMatrixInit;
from matrixUpdate import featureWeightPanelUpdate;
from matrixUpdate import weightMatrixUpdate;
from matrixEntropyFun import matrixEntropyFun;
from harmonicFun import harmonicFun;
from AffinityFunPanelInit import AffinityFunSubMatrixInit;
from AffinityFunPanelInit import linearizeFun;
from AffinityFunPanelInit import AffinityFunPanelInit;

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
          labeledFeatureMatrix,
          unlabeledFeatureMatrix):
    
    # initialize Pu
    unlabeledDistriMatrix = unlabeledDistriMatrixInit(unlabeledList, MAX_AQI + 1);
    
    # construct labeledDistriMatrix Pv from labeledAQIDict
    labeledDistriMatrix = labeledDistriMatrixInit(labeledAQIDict, MAX_AQI + 1);

    # construct the node list
    nodeList = labeledList + unlabeledList;
    
    # construct AffinityFunMatrix list from featureDict list
    AffinityFunPanel = AffinityFunPanelInit(nodeList,
                                            labeledFeatureMatrix,
                                            unlabeledFeatureMatrix,
                                            labeledAQIDict);

    # initialize feature weight matrix
    featureWeightMatrixDict = OrderedDict();

    for feature in labeledFeatureMatrix.columns:
        featureWeightMatrixDict[feature] = stringIndexMatrixInit(nodeList, nodeList, 1.0);

    featureWeightPanel = pd.Panel(featureWeightMatrixDict);

    # update weight matrix
    weightMatrix = weightMatrixUpdate(featureWeightPanel, AffinityFunPanel);

    # calculate old entropy H(Pu)
    lastUnlabeledDistriEntropy = matrixEntropyFun(unlabeledDistriMatrix);

    # assign the old entropy H(Pu) to diff(H(Pu)) and start iteration
    unlabeledDistriEntropyDiff = lastUnlabeledDistriEntropy;

    # iteration starts:
    while unlabeledDistriEntropyDiff > CONV_THRESHOLD:
    
        # update Pik matrix
        featureWeightPanelUpdate(featureWeightPanel, weightMatrix, AffinityFunPanel);

        # update weight matrix
        weightMatrix = weightMatrixUpdate(featureWeightPanel, AffinityFunPanel);

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
