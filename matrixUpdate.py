# libs
from collections import OrderedDict
import math

def featureWeightPanelUpdate(featureWeightPanel, weightMatrix, AffinityFunPanel):
    
    for feature in featureWeightPanel.items:
        featureWeightPanel[feature] = (1.0 - 2.0 * weightMatrix * \
                                       AffinityFunPanel[feature]) * \
                                       featureWeightPanel[feature]

def weightMatrixUpdate(featureWeightPanel, AffinityFunPanel):

    tempMatrixDict = OrderedDict()

    for feature in featureWeightPanel.items:
        tempMatrixDict[feature] = featureWeightPanel[feature] * \
                                  featureWeightPanel[feature] * \
                                  AffinityFunPanel[feature]

    tempWeightMatrix = - sum(tempMatrixDict.values())
    
    return tempWeightMatrix.applymap(math.exp)

def weightMatrixFilter(weightMatrix, labeledList):
    
    weightMatrix.ix[labeledList, labeledList] = 0.0
