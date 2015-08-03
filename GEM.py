import pandas as pd;
from AQInf import AQInf;
from minEntropyNodeInfer import minEntropyNodeInfer;
from matrixInit import stringIndexMatrixInit;

# Input:
# (a) [string list] a set of locations V with existing measurement stations;
# (b) [string list] a set of candidate locations C without stations;
# (c) [string list] the time stamps T = t1, t2,...,tm;
# (d) [int] the number of locations k to be selected for new stations;
# Output:
# [string list] the set S of k recommended locations (|S| = k);

###########################
# haven't implemented:
# [optional] algo.2.12: sum finished, average
# labeledAQIDict: AQInf's para, the Pv matrix, feed input into it. 
###########################

def GEM(labeledList, unlabeledList, timeStampList, numToBeRecommend):
    
    # variables
    unlabeledListLen = len(unlabeledList);
    
    # initialize the rankTable
    # unlabeled nodes -> time stamps
    rankTable = pd.DataFrame([ [-1] * len(unlabeledList) ] * len(timeStampList),
                             index = timeStampList,
                             columns = unlabeledList);

    # for each time stamps: do GEM
    for currentTimeStamp in timeStampList:

        leftUnlabeledList = unlabeledList;
        
        # for each unlabeled nodes: do GEM
        for currentRank in range(unlabeledListLen, 0, -1):

            unlabeledDistriMatrix = AQInf(labeledList, leftUnlabeledList, currentTimeStamp, labeledAQIDict);

            # select the unlabedled node with the min entropy
            (minEntropyUnlabeled, minEntropyUnlabeledAQI) = minEntropyNodeInfer(unlabeledDistriMatrix);

            # give the rank value reversely
            rankTable[minEntropyUnlabeled][currentTimeStamp] = currentRank;

            # turn unlabeled to labeled
            labeledList.append(minEntropyUnlabeled);

            # append the new inferred AQI
            labeledAQIDict[minEntropyUnlabeled] = minEntropyUnlabeledAQI;

            # exclude the labeled node from the unlabeled list
            unlabeledList.remove(minEntropyUnlabeled);

    # construct the recommend list
    # sort the rankList in descending order
    return list(pd.DataFrame(rankTable.sum()).sort(columns = 0, ascending = False).index);
