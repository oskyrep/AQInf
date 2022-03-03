#!/usr/bin/python

#import pdb
#pdb.set_trace()

#import cProfile

import sys

from GEM import GEM
from inputManage import inputManage

argv = ['dummy','input/labeledList', 'input/unlabeledList', 'input/timeStampList',
        'input/featureList', 'input/labeledAQITable.csv', 'input/labeledFeatureTimeStampPanel.csv',
        'input/unlabeledFeatureTimeStampPanel.csv','10']

if __name__ == '__main__':

    (labeledList,
     unlabeledList,
     timeStampList,
     featureList,
     labeledAQITable,
     labeledFeatureTimeStampPanel,
     unlabeledFeatureTimeStampPanel,
     numToBeRecommend) = inputManage(argv)

    recommendList = GEM(labeledList,
                        unlabeledList,
                        timeStampList,
                        featureList,
                        labeledAQITable,
                        labeledFeatureTimeStampPanel,
                        unlabeledFeatureTimeStampPanel,
                        numToBeRecommend)

    print(recommendList)


