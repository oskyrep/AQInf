#!/usr/bin/python

# libs
import pandas as pd
import numpy as np
from collections import OrderedDict
    # linear regression
from sklearn.linear_model import LinearRegression
    # euclidean distance
import math

# constants
from constants import *
import accelerator
import itertools

def commonDiffMatrixCore(featurePair):
    return featurePair[0] - featurePair[1]

def commonDiffMatrixInit(featureList1, featureList2):
    #tempArray = list(accelerator.pool_obj.map(commonDiffMatrixCore, list(itertools.product(featureList1, featureList2))))
    tempArray = np.subtract(np.tile(np.array(list(featureList1)), (len(featureList2), 1)),
                np.tile(np.array(list(featureList2)), (len(featureList1), 1)).T)
    # featureList1 = np.array(list(featureList1))
    #
    # featureList2 = np.array(list(featureList2)).reshape(-1, 1)
    # out = None
    # it = np.nditer([featureList1, featureList2, out],
    #                [],
    #                [['readonly'], ['readonly'], ['writeonly', 'allocate']])
    #
    # subOp = np.subtract
    # with it:
    #     for (x, y, z) in it:
    #         subOp(x, y, out = z)
    #
    #     return abs(it.operands[2])
    return abs(tempArray)

def geoDiffMatrixInit(featureList1, featureList2):

    #tempArray = list(accelerator.pool_obj.map(geoDiffMatrixCore, list(itertools.product(featureList2, featureList1))))
    featureList11 = [i[0] for i in featureList1]
    featureList22 = [i[1] for i in featureList2]
    tempFeatureArray1 = np.tile(np.array(featureList1), (len(featureList2), 1))
    tempFeatureArray2 = np.repeat(featureList2, len(featureList1), axis=0)
    tempFeatureArray = tempFeatureArray2 - tempFeatureArray1
    tempArray = np.hypot(tempFeatureArray.T[0], tempFeatureArray.T[1])
    # for node2 in featureList2:
    #     for node1 in featureList1:
    #         tempArray.append(math.hypot( eval(node1)[0] - eval(node2)[0], eval(node1)[1] - eval(node2)[1] ))

    return tempArray.reshape(len(featureList2), len(featureList1))

def linearizeFun(entity, slope, intercept):
    
    return slope * entity + intercept

def AffinityFunPanelInit(nodeList,
                         labeledFeatureMatrix,
                         unlabeledFeatureMatrix,
                         labeledAQIDict):
    
    tempMatrixDict = OrderedDict()

    # construct labeled AQI array
    # has nothing to do with loops
    AQIList = labeledAQIDict.values()
    labeledAQIDiffArray = commonDiffMatrixInit(AQIList, AQIList).ravel()
    funDict = {

        'commonDiffMatrixInit': commonDiffMatrixInit,
        'geoDiffMatrixInit': geoDiffMatrixInit
    }

    def fff(feature):
    #for feature in labeledFeatureMatrix.columns:

        lList = list(labeledFeatureMatrix[feature])
        uList = list(unlabeledFeatureMatrix[feature])
        
        # function pointer
        if feature == 'rowCol':
            funChosen = 'geoDiffMatrixInit'
            lList = list(map(eval, lList))
            uList = list(map(eval, uList))
        else:
            funChosen = 'commonDiffMatrixInit'

        tempMatrix = np.vstack( ( np.hstack([funDict[funChosen](lList, lList),
                                             funDict[funChosen](uList, lList)]),
                                  np.hstack([funDict[funChosen](lList, uList),
                                             funDict[funChosen](uList, uList)]) ) )
        
        # get (slope, intercept) from linear regression
        labeledFeatureDiffArray = funDict[funChosen](lList, lList).ravel()

        # linear regression
        model = LinearRegression(fit_intercept=False).fit(labeledFeatureDiffArray.reshape((-1, 1)), labeledAQIDiffArray)

        entityLinearizeFun = np.vectorize(linearizeFun, otypes=[np.float])

        tempMatrix = entityLinearizeFun(tempMatrix, model.coef_, model.intercept_)
        
        tempMatrix = NORMALIZE_FACTOR * (tempMatrix - tempMatrix.min()) / (tempMatrix.max() - tempMatrix.min())

        tempMatrixList = pd.DataFrame(tempMatrix,
                                               index = nodeList,
                                               columns = nodeList,
                                               dtype = float)
        return tempMatrixList

    #tempMatrixList = accelerator.pool_obj.map(fff, list(labeledFeatureMatrix.columns))
    tempMatrixList = map(fff, list(labeledFeatureMatrix.columns))
    tempMatrixDict = dict(zip(list(labeledFeatureMatrix.columns), tempMatrixList))
    tempMatrixPanel = pd.Panel(tempMatrixDict)

    # for key in tempMatrixPanel.keys():
    #     if key == 'rowCol':
    #         tempMatrixPanel[key] = tempMatrixPanel[key] * 10
    return tempMatrixPanel
