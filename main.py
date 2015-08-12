import pdb;
pdb.set_trace();

from allInputs import *;

from GEM import GEM;

if __name__ == '__main__':
    
    recommendList = GEM(labeledList,
                        unlabeledList,
                        timeStampList,
                        labeledAQITable,
                        labeledFeatureDictListUponTimeStamp,
                        unlabeledFeatureDictListUponTimeStamp,
                        numToBeRecommend);

    print recommendList;
