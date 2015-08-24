#!/usr/bin/python

# libs
import pandas as pd;
from collections import OrderedDict;
import itertools;

# functions
from AQInf import AQInf;
from minEntropyNodeInfer import minEntropyNodeInfer;

# Input:
# (a) [string list] the labeled node list
# (b) [string list] the unlabeled node list
# (c) [string list] the time stamp list
# (d) [pandas DataFrame] the AQI value of labeled node over time stamp
# (e) [int] the # of locations k to be selected for new stations
# Output:
# [string list] the set S of k recommended locations (|S| = k)

# haven't implemented:
# [optional] algo.2.12: sum finished, average
# labeledAQIDict: AQInf's para, the Pv matrix, feed input into it. 

def GEM(labeledList,
        unlabeledList,
        timeStampList,
        featureList,
        labeledAQITable,
        labeledFeatureTimeStampPanel,
        unlabeledFeatureTimeStampPanel,
        numToBeRecommend):
    
    # variables
    unlabeledListLen = len(unlabeledList);
    currentLabeledList = [];
    labeledAQIDict = OrderedDict();
    labeledFeatureMatrix = pd.DataFrame(columns = featureList);
    
    # initialize the rankTable
    # unlabeled nodes -> time stamps
    rankTable = pd.DataFrame([ [-1] * unlabeledListLen ] * len(timeStampList),
                             index = timeStampList,
                             columns = unlabeledList);

    # combine the 2 node list with time stamp list
    labeledList = list( itertools.product(timeStampList, labeledList) );
    unlabeledList = list( itertools.product(timeStampList, unlabeledList) );

    # begin iteration 
    for currentTimeStamp in timeStampList:

        # update the 2 node list each time stamp
        tempLabeledList = [ element for element in labeledList if element[0] == currentTimeStamp ];
        currentLabeledList += tempLabeledList;

        leftUnlabeledList = [ element for element in unlabeledList if element[0] == currentTimeStamp ];

        # update the 2 feature DataFrame
        tempLabeledFeatureMatrix = labeledFeatureTimeStampPanel[currentTimeStamp].copy();
        tempLabeledFeatureMatrix.index = tempLabeledList;
        labeledFeatureMatrix = labeledFeatureMatrix.append(tempLabeledFeatureMatrix);

        unlabeledFeatureMatrix = unlabeledFeatureTimeStampPanel[currentTimeStamp].copy();
        unlabeledFeatureMatrix.index = leftUnlabeledList;

        # update the labeled AQI dict each time stamp
        tempLabeledAQIDict = OrderedDict( zip( tempLabeledList, 
                                               labeledAQITable[ currentTimeStamp : currentTimeStamp ].
                                               values.ravel().tolist() ) );
        labeledAQIDict.update(tempLabeledAQIDict);
        
        # for each unlabeled nodes: do GEM
        for currentRank in range(unlabeledListLen, 0, -1):

            unlabeledDistriMatrix = AQInf(currentLabeledList,
                                          leftUnlabeledList,
                                          currentTimeStamp,
                                          labeledAQIDict,
                                          labeledFeatureMatrix,
                                          unlabeledFeatureMatrix);

            # select the unlabedled node with the min entropy
            (minEntropyUnlabeled, minEntropyUnlabeledAQI) = minEntropyNodeInfer(unlabeledDistriMatrix);

            # give the rank value reversely
            rankTable[ minEntropyUnlabeled[1] ][currentTimeStamp] = currentRank;

            # turn unlabeled to labeled
            currentLabeledList.append(minEntropyUnlabeled);

            # update the labeled AQI dict
            labeledAQIDict[minEntropyUnlabeled] = minEntropyUnlabeledAQI;

            # exclude the labeled node from the unlabeled list
            leftUnlabeledList.remove(minEntropyUnlabeled);

            # update the 2 feature panels
            labeledFeatureMatrix = labeledFeatureMatrix.append(unlabeledFeatureMatrix[minEntropyUnlabeled : minEntropyUnlabeled]);
            unlabeledFeatureMatrix.drop(minEntropyUnlabeled, inplace = True);

    # output the rankTable
    outputRankTableFileName = 'rankTable.csv';
    rankTable.to_csv(outputRankTableFileName);

    # output the labeled AQI Table
    outputLabeledAQITableFileName = 'labeledAQITable.csv';
    pd.DataFrame([labeledAQIDict]).to_csv(outputLabeledAQITableFileName);
 
    # output the recommend list
    outputRecommendListFile = open('recommendList', "w");
    for string in list(pd.DataFrame(rankTable.sum()).sort(columns = 0).index):
        outputRecommendListFile.write("%s\n" % string);

    # construct the recommend list
    # sort the rankList in descending order
    return list(pd.DataFrame(rankTable.sum()).sort(columns = 0).index)[:numToBeRecommend];
