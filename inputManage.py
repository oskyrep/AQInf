import pandas as pd;

def inputManage(argv):

    # parsing inputs
    labeledListFileName = argv[1];
    unlabeledListFileName = argv[2];
    timeStampListFileName = argv[3];
    featureListFileName = argv[4];
    labeledAQITableFileName = argv[5];
    labeledFeatureTimeStampPanelFileName = argv[6];
    unlabeledFeatureTimeStampPanelFileName = argv[7];
    numToBeRecommend = int(argv[8]);

    # labeledList
    with open(labeledListFileName) as labeledListFile:
        labeledList = labeledListFile.read().splitlines();

    # unlabeledList
    with open(unlabeledListFileName) as unlabeledListFile:
        unlabeledList = unlabeledListFile.read().splitlines();

    # timeStampList
    with open(timeStampListFileName) as timeStampListFile:
        timeStampList = timeStampListFile.read().splitlines();

    # featureList
    with open(featureListFileName) as featureListFile:
        featureList = featureListFile.read().splitlines();

    # labeledAQITable
    labeledAQITable = pd.read_csv(labeledAQITableFileName);

    # labeledFeatureTimeStampPanel(need to be modified)
    labeledFeatureTimeStampDataFrame = pd.read_csv(labeledFeatureTimeStampPanelFileName);
    labeledFeatureTimeStampPanel = pd.Panel({'t1':labeledFeatureTimeStampDataFrame});

    # unlabeledFeatureTimeStampPanel(need to be modified)
    unlabeledFeatureTimeStampDataFrame = pd.read_csv(unlabeledFeatureTimeStampPanelFileName);
    unlabeledFeatureTimeStampPanel = pd.Panel({'t1':unlabeledFeatureTimeStampDataFrame});

    return (labeledList,
            unlabeledList,
            timeStampList,
            featureList,
            labeledAQITable,
            labeledFeatureTimeStampPanel,
            unlabeledFeatureTimeStampPanel,
            numToBeRecommend);
