# libs
from collections import OrderedDict;
import math;

# Input:
# (a) [list of pandas DataFrame] the list of feature weight matrix
# (b) [pandas DataFrame] the weight matrix
# (c) [list of pandas DataFrame] the list of Affinity Function matrix
# Output:
# None, the operation is done on (a)

def featureWeightPanelUpdate(featureWeightPanel, weightMatrix, AffinityFunPanel):
    
    for feature in featureWeightPanel.items:
        featureWeightPanel[feature] = (1.0 - 2.0 * weightMatrix * \
                                       AffinityFunPanel[feature]) * \
                                       featureWeightPanel[feature];

# Input:
# (a) [list of pandas DataFrame] the list of feature weight matrix
# (b) [list of pandas DataFrame] the list of Affinity Function matrix
# Output:
# [pandas DataFrame] the updated weight matrix

def weightMatrixUpdate(featureWeightPanel, AffinityFunPanel):

    tempMatrixDict = OrderedDict();

    for feature in featureWeightPanel.items:
        tempMatrixDict[feature] = featureWeightPanel[feature] * \
                                  featureWeightPanel[feature] * \
                                  AffinityFunPanel[feature];

    tempWeightMatrix = - sum(tempMatrixDict.values());
    
    return tempWeightMatrix.applymap(math.exp);

def weightMatrixFilter(weightMatrix, labeledList):
    
    weightMatrix.ix[labeledList, labeledList] = 0.0;
