#!/usr/bin/python

import sys;
import pandas as pd;

if __name__ == '__main__':
    
    inputNodeFeatureDataFrameFileName = sys.argv[1];
    outputTimeNodeAQIDataFrameFileName = sys.argv[2];
    
    nodeFeatureDataFrame = pd.read_csv(inputNodeFeatureDataFrameFileName);

    nodeFeatureDataFrame.ix[ : , 'PM10' : 'PM10' ].T.to_csv(outputTimeNodeAQIDataFrameFileName);
