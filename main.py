import copy

import finGp

from scipy import stats

firstTractorH = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/hshare/0038.HK.csv",shareCode='0038.HK')
firstTractorA = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/ashare/601038.SH.csv",shareCode='601038.SH')
newsSentiment = finGp.creator.NewsCollectionCreator.getInstacnefromCsv("example_data/sentiment/test_data.csv",shareCode='0038.HK')


firstTractorA.joinGroupTable(newsSentiment)
firstTractorH.joinGroupTable(newsSentiment)


def carDiff(gPointA,gPointB):     
    newPoint = copy.copy(gPointA)
    cardiff = gPointA.cumulativeAbnormalReturn-gPointB.cumulativeAbnormalReturn
    if cardiff < 0 : 
        cardiff = cardiff*-1
    newPoint.__cumulativeAbnormalReturn = cardiff
    return newPoint
    

comparisonGroup = finGp.Group(
    firstTractorA.shareEntity,
    finGp.Group.operateElementwiseInAClassSpace(
        firstTractorA,
        firstTractorH,
        finGp.element.CarNElement,
        carDiff)
)

finGp.Group.normalizeAllGroups(firstTractorA,firstTractorH)









#Part 1: Normality test 

##List of Car DataPoint 
aCarPoints = firstTractorA.getElement(finGp.element.CarNElement(interval=3))
hCarPoints = firstTractorH.getElement(finGp.element.CarNElement(interval=3))
###List of cumulativeAbnormalReturn
aCar = [x.cumulativeAbnormalReturn for x in aCarPoints]
hCar = [x.cumulativeAbnormalReturn for x in hCarPoints]



##List of CarNews DataPoint
aCarNew = firstTractorA.getElement(finGp.element.CarNewsElement)
hCarNew = firstTractorH.getElement(finGp.element.CarNewsElement)


    

         
    

resACar = stats.normaltest(aCar)
print("aCar pValue:",resACar.pvalue)

resHCar = stats.normaltest(hCar)
print("hCar pValue:",resHCar.pvalue)

resACarWithNews = stats.normaltest(aCarWithNews)
print("aCar with News pValue:",resACarWithNews.pvalue)

resHCarWithNews = stats.normaltest(hCarWithNews)
print("hCar with News pValue:",resHCarWithNews.pvalue)



