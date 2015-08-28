#!/usr/bin/python

# import pdb;
# pdb.set_trace();

import cProfile;

import sys;

from GEM import GEM;
from inputManage import inputManage;

if __name__ == '__main__':

    (labeledList,
     unlabeledList,
     timeStampList,
     featureList,
     labeledAQITable,
     labeledFeatureTimeStampPanel,
     unlabeledFeatureTimeStampPanel,
     numToBeRecommend) = inputManage(sys.argv);

    recommendList = GEM(labeledList,
                        unlabeledList,
                        timeStampList,
                        featureList,
                        labeledAQITable,
                        labeledFeatureTimeStampPanel,
                        unlabeledFeatureTimeStampPanel,
                        numToBeRecommend);

    print recommendList;
