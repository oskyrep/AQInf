import collections;

# Input:
# [2D dict]
# Output:
# [2D list]
def twoDimDictToTwoDimList(twoDimDict):
    return [ [ twoDimDict[row][col] for col in twoDimDict[row] ] for row in twoDimDict ];

# Input:
# [2D list]
# Output:
# [2D dict]
def twoDimListToTwoDimDict(twoDimList, rowIndexList):
    return collections.OrderedDict(zip(rowIndexList, twoDimList));
