#!/usr/bin/python

# libs
import pandas as pd
from collections import OrderedDict
import itertools

# functions
from AQInf import AQInf
from minEntropyNodeInfer import minEntropyNodeInfer

import time

import accelerator
import multiprocessing
from pathos.multiprocessing import ProcessingPool as Pool


def GEM(labeledList,
        unlabeledList,
        timeStampList,
        featureList,
        labeledAQITable,
        labeledFeatureTimeStampPanel,
        unlabeledFeatureTimeStampPanel,
        numToBeRecommend):
    

    # variables
    unlabeledListLen = len(unlabeledList)
    superCurrentLabeledList = []
    superLabeledAQIDict = OrderedDict()
    superLabeledFeatureMatrix = pd.DataFrame(columns = featureList)

    #accelerator.pool_obj = Pool()

    # initialize the rankTable
    # unlabeled nodes -> time stamps
    rankTable = pd.DataFrame([ [-1] * unlabeledListLen ] * len(timeStampList),
                             index = timeStampList,
                             columns = unlabeledList)

    # combine the 2 node list with time stamp list
    labeledList = list( itertools.product(timeStampList, labeledList) )
    unlabeledList = list( itertools.product(timeStampList, unlabeledList) )

    rankedList = []

    # begin iteration
    for currentTimeStamp in timeStampList:

        # update the 2 node list each time stamp
        tempLabeledList = [ element for element in labeledList if element[0] == currentTimeStamp ]
        #currentLabeledList += tempLabeledList
        superCurrentLabeledList = tempLabeledList

        superLeftUnlabeledList = [ element for element in unlabeledList if element[0] == currentTimeStamp ]

        # update the 2 feature DataFrame
        tempLabeledFeatureMatrix = labeledFeatureTimeStampPanel[currentTimeStamp].copy()
        tempLabeledFeatureMatrix.index = tempLabeledList
        superLabeledFeatureMatrix = superLabeledFeatureMatrix.append(tempLabeledFeatureMatrix)

        superUnlabeledFeatureMatrix = unlabeledFeatureTimeStampPanel[currentTimeStamp].copy()
        superUnlabeledFeatureMatrix.index = superLeftUnlabeledList

        # update the labeled AQI dict each time stamp
        tempLabeledAQIDict = OrderedDict( zip( tempLabeledList,
                                               labeledAQITable[ currentTimeStamp : currentTimeStamp ].
                                               values.ravel().tolist() ) )
        superLabeledAQIDict.update(tempLabeledAQIDict)
        funcstarttime = time.time()
        # for each unlabeled nodes: do GEM
        count_iter = 0
        minEntropyUnlabeled = 0
        minEntropyUnlabeledAQI = 0

        for superRank in range(numToBeRecommend):

            currentLabeledList = superCurrentLabeledList.copy()
            labeledAQIDict = superLabeledAQIDict.copy()
            leftUnlabeledList = superLeftUnlabeledList.copy()
            labeledFeatureMatrix = superLabeledFeatureMatrix.copy()
            unlabeledFeatureMatrix = superUnlabeledFeatureMatrix.copy()
            count_iter = 0
            for currentRank in range(len(leftUnlabeledList), 0, -1):
                count_iter = count_iter +1
                print(count_iter)
                print("------------------------start time: %d------------------------" % funcstarttime)
                unlabeledDistriMatrix = AQInf(currentLabeledList,
                                              leftUnlabeledList,
                                              currentTimeStamp,
                                              labeledAQIDict,
                                              labeledFeatureMatrix,
                                              unlabeledFeatureMatrix)

                nowtime = time.time() - funcstarttime
                funcstarttime = time.time()
                print("------------------------AQInf time: %d------------------------" % nowtime)
                # select the unlabedled node with the min entropy
                (minEntropyUnlabeled, minEntropyUnlabeledAQI) = minEntropyNodeInfer(unlabeledDistriMatrix)
                print("minimum entropy unlabeled: {}".format(minEntropyUnlabeled))
                # give the rank value reversely
                #rankTable[ minEntropyUnlabeled[1] ][currentTimeStamp] = currentRank

                # turn unlabeled to labeled
                currentLabeledList.append(minEntropyUnlabeled)

                # update the labeled AQI dict
                labeledAQIDict[minEntropyUnlabeled] = minEntropyUnlabeledAQI

                # exclude the labeled node from the unlabeled list
                leftUnlabeledList.remove(minEntropyUnlabeled)

                # update the 2 feature panels
                labeledFeatureMatrix = labeledFeatureMatrix.append(unlabeledFeatureMatrix[minEntropyUnlabeled : minEntropyUnlabeled])
                unlabeledFeatureMatrix.drop(minEntropyUnlabeled, inplace = True)

            # add the least rank node to final rank table
            rankTable[minEntropyUnlabeled[1]][currentTimeStamp] = superRank + 1

            rankedList.append(minEntropyUnlabeled[1])

            superCurrentLabeledList.append(minEntropyUnlabeled)
            superLabeledAQIDict[minEntropyUnlabeled] = minEntropyUnlabeledAQI
            superLeftUnlabeledList.remove(minEntropyUnlabeled)
            superLabeledFeatureMatrix = superLabeledFeatureMatrix.append(
                labeledFeatureMatrix[minEntropyUnlabeled: minEntropyUnlabeled])
            superUnlabeledFeatureMatrix.drop(minEntropyUnlabeled, inplace=True)


    print(rankedList)
    # rankTable = pd.read_csv('rankTable.csv')
    # rankTable.set_index(rankTable.columns[0], inplace = True)
    # return list(pd.DataFrame(rankTable.sum()).sort(columns = 0).index)[:numToBeRecommend]

    # output the rankTable
    outputRankTableFileName = 'rankTable.csv'
    rankTable.to_csv(outputRankTableFileName)

    # output the labeled AQI Table
    outputLabeledAQITableFileName = 'labeledAQITable.csv'
    pd.DataFrame([labeledAQIDict]).to_csv(outputLabeledAQITableFileName)
 
    # output the recommend list
    outputRecommendListFile = open('recommendList', "w")
    for string in list(pd.DataFrame(rankTable).sort_values(by = ['t1'],axis = 1)):
        outputRecommendListFile.write("%s\n" % string)

    # construct the recommend list
    # sort the rankList in descending order
    return list(pd.DataFrame(rankTable).sort_values(by = ['t1'],axis = 1))[:numToBeRecommend]
