#!/usr/bin/python

import sys;
import pandas as pd;

if __name__ == '__main__':

    inputNodeFeatureDataFrameFileName = sys.argv[1];
    outputNodeListFile = open(sys.argv[2], "w");
    
    nodeFeatureDataFrame = pd.read_csv(inputNodeFeatureDataFrameFileName);

    for string in list(nodeFeatureDataFrame.index):
        outputNodeListFile.write("%s\n" % string);
