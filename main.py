import copy
import math

from group_creator import PricingCollectionCreator,NewsCollectionCreator
from group import Group
import point

firstTractorH = PricingCollectionCreator.getInstacnefrom("example_data/hshare/0038.HK.csv")
firstTractorA = PricingCollectionCreator.getInstacnefrom("example_data/ashare/601038.SH.csv")
newsSentiment = NewsCollectionCreator.getInstacnefrom("example_data/sentiment/test_data.csv")


firstTractorA.joinGroupTable(newsSentiment)
firstTractorH.joinGroupTable(newsSentiment)

for i in firstTractorA.valuedSubgroup: 
    print("valued ",i)

def carDiff(gPointA,gPointB): 
    
    newPoint = copy.copy(gPointA)
    cardiff = gPointA.cumulativeAbnormalReturn-gPointB.cumulativeAbnormalReturn
    if cardiff < 0 : 
        cardiff = cardiff*-1
    newPoint.cumulativeAbnormalReturn=cardiff
    return newPoint
    

comparisonGroup = Group(
    firstTractorA.shareEntity,
    Group.operateElementwiseInAClassSpace(
        firstTractorA,
        firstTractorH,
        point.CarNDataPoint,
        carDiff)
)


