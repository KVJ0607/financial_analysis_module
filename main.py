import copy

import finGp

firstTractorH = finGp.group_creator.PricingCollectionCreator.getInstacnefrom("example_data/hshare/0038.HK.csv")
firstTractorA = finGp.group_creator.PricingCollectionCreator.getInstacnefrom("example_data/ashare/601038.SH.csv")
newsSentiment = finGp.group_creator.NewsCollectionCreator.getInstacnefrom("example_data/sentiment/test_data.csv")


firstTractorA.joinGroupTable(newsSentiment)
firstTractorH.joinGroupTable(newsSentiment)


def carDiff(gPointA,gPointB):     
    newPoint = copy.copy(gPointA)
    cardiff = gPointA.cumulativeAbnormalReturn-gPointB.cumulativeAbnormalReturn
    if cardiff < 0 : 
        cardiff = cardiff*-1
    newPoint.cumulativeAbnormalReturn=cardiff
    return newPoint
    

comparisonGroup = finGp.Group(
    firstTractorA.shareEntity,
    finGp.Group.operateElementwiseInAClassSpace(
        firstTractorA,
        firstTractorH,
        finGp.element_of_group.CarNElement,
        carDiff)
)




