#!/usr/bin/python

import sys;
import pandas as pd;

if __name__ == '__main__':

    inputNodeFeatureDataFrameFileName = sys.argv[1];
    outputNodeFeatureDataFrameFileName = sys.argv[2];
    outputFeatureListFile = open(sys.argv[3], "w");
    
    nodeFeatureDataFrame = pd.read_csv(inputNodeFeatureDataFrameFileName);

    nodeFeatureDataFrame = nodeFeatureDataFrame[['rowCol', 'hw_len', 'rd_len', 'num_intersection']];
    nodeFeatureDataFrame.to_csv(outputNodeFeatureDataFrameFileName);

    for string in list(nodeFeatureDataFrame.columns)[:]:
        outputFeatureListFile.write("%s\n" % string);
