import collections;

# Input:
# [2D dict]
# Output:
# [2D list]

def twoDimDictToTwoDimList(twoDimDict):
    return [ [ twoDimDict[row][col] for col in twoDimDict[row] ] for row in twoDimDict ];

# Input:
# (a) [2D list]
# (b) [string list] the row Index list
# Output:
# [2D dict]

def twoDimListToTwoDimDict(twoDimList, rowIndexList):
    return collections.OrderedDict( zip(rowIndexList, twoDimList) );
