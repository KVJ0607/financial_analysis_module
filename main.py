import copy

import finGp

from scipy import stats

firstTractorH = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/hshare/0038.HK.csv",shareCode='0038.HK')
firstTractorA = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/ashare/601038.SH.csv",shareCode='601038.SH')
newsSentiment = finGp.creator.NewsCollectionCreator.getInstacnefromCsv("example_data/sentiment/test_data.csv",shareCode='0038.HK')

print("firstA:")
print(firstTractorA)
print("")
print("firstH:")
print(firstTractorH)
print("")
print("news:")
print(newsSentiment)
print("")
print("")

firstTractorA.joinGroupTable(newsSentiment)
firstTractorH.joinGroupTable(newsSentiment)

print("Joined A:")
print(firstTractorA)
print("")
print("Joined H:")
print(firstTractorH)
print("")
print("")

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

print("Joined normalized A:")
print(firstTractorA)
print("")
print("Joined normalized H:")
print(firstTractorH)
print("")

##Part 1: Normality test 
a_car = firstTractorA.getDataPoins(finGp.element.CarNElement)
a_car = [x.cumulativeAbnormalReturn for x in a_car]
h_car = firstTractorH.getDataPoins(finGp.element.CarNElement)
h_car = [x.cumulativeAbnormalReturn for x in h_car]


res_a_car = stats.normaltest(a_car)
print(res_a_car.statistic)
print(res_a_car.pvalue)


res_h_car = stats.normaltest(a_car)
print(res_h_car.statistic)
print(res_h_car.pvalue)

###Part 2: Normality test on the CarNews
# a_carNews = firstTractorA.getDataPoins(finGp.element.PricingElement)
# h_carNews = firstTractorH.getDataPoins(finGp.element.PricingElement)

# res_a_carNews = stats.normaltest(a_carNews)
# res_a_carNews.statistic
# res_a_carNews.pvalue


# res_h_carNews = stats.normaltest(a_carNews)
# res_h_carNews.statistic
# res_h_carNews.pvalue
