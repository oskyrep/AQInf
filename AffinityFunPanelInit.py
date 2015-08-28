#!/usr/bin/python

# libs
import pandas as pd;
import numpy as np;
from collections import OrderedDict;
    # linear regression
from scipy import stats;
    # euclidean distance
import math;

# constants
from constants import *;

# Input:
# (a) [float list] feature list 1
# (b) [float list] feature list 2
# Output:
# [numpy matrix] sub Affinity Function matrix after operation

def commonDiffMatrixInit(featureList1, featureList2):

    featureList1 = np.array(featureList1);

    featureList2 = np.array(featureList2).reshape(-1, 1);

    it = np.nditer([featureList1, featureList2, None],
                   [],
                   [['readonly'], ['readonly'], ['writeonly', 'allocate']]);

    subOp = np.subtract;

    for x, y, z in it:
        subOp(x, y, out = z);

    return abs(it.operands[2]);

def geoDiffMatrixInit(featureList1, featureList2):

    tempArray = [];

    for node2 in featureList2:
        for node1 in featureList1:
            tempArray.append(math.hypot( eval(node1)[0] - eval(node2)[0], eval(node1)[1] - eval(node2)[1] ));

    return np.array(tempArray).reshape(len(featureList2), len(featureList1));

# Input:
# (a) [float] numpy matrix's entity
# (b) [float] linear function slope
# (c) [float] linear function intercept
# Output:
# [float] new numpy matrix's entity after linearization

def linearizeFun(entity, slope, intercept):
    
    return slope * entity + intercept;

# Input:
# (a) [string list] the node list (labeled + unlabeled)
# (b) [list of dict] the list of labeled node feature dicts ([dict] labeled : feature value)
# (c) [list of dict] the list of unlabeled node feature dicts ([dict] unlabeled : feature value)
# (d) [float] the # of features
# (e) [dict] labeled : AQI
# Output:
# [list of dict] the Affinity Function matrix after initialization

def AffinityFunPanelInit(nodeList,
                         labeledFeatureMatrix,
                         unlabeledFeatureMatrix,
                         labeledAQIDict):
    
    tempMatrixDict = OrderedDict();

    # construct labeled AQI array
    # has nothing to do with loops
    AQIList = labeledAQIDict.values();
    labeledAQIDiffArray = commonDiffMatrixInit(AQIList, AQIList).ravel();

    funDict = {
        
        'commonDiffMatrixInit': commonDiffMatrixInit,
        'geoDiffMatrixInit': geoDiffMatrixInit
    };
    
    for feature in labeledFeatureMatrix.columns:

        lList = list(labeledFeatureMatrix[feature]);
        uList = list(unlabeledFeatureMatrix[feature]);
        
        # function pointer
        if feature == 'rowCol':
            funChosen = 'geoDiffMatrixInit';
        else:
            funChosen = 'commonDiffMatrixInit';

        tempMatrix = np.vstack( ( np.hstack([funDict[funChosen](lList, lList),
                                             funDict[funChosen](uList, lList)]),
                                  np.hstack([funDict[funChosen](lList, uList),
                                             funDict[funChosen](uList, uList)]) ) );
        
        # get (slope, intercept) from linear regression
        labeledFeatureDiffArray = funDict[funChosen](lList, lList).ravel();

        # linear regression
        regressResult = stats.linregress(labeledFeatureDiffArray, labeledAQIDiffArray);

        entityLinearizeFun = np.vectorize(linearizeFun, otypes=[np.float]);

        tempMatrix = entityLinearizeFun(tempMatrix, regressResult[0], regressResult[1]);
        
        tempMatrix = NORMALIZE_FACTOR * (tempMatrix - tempMatrix.min()) / (tempMatrix.max() - tempMatrix.min());

        tempMatrixDict[feature] = pd.DataFrame(tempMatrix,
                                               index = nodeList,
                                               columns = nodeList,
                                               dtype = float);

    return pd.Panel(tempMatrixDict);
