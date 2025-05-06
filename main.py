import copy

import finGp

from scipy import stats

firstTractorH = finGp.group_creator.PricingCollectionCreator.getInstacnefromCsv("example_data/hshare/0038.HK.csv")
firstTractorA = finGp.group_creator.PricingCollectionCreator.getInstacnefromCsv("example_data/ashare/601038.SH.csv")
newsSentiment = finGp.group_creator.NewsCollectionCreator.getInstacnefromCsv("example_data/sentiment/test_data.csv")


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

#finGp.Group.normalizeAllGroups(firstTractorA,firstTractorH)

for k,v in firstTractorA.cayleyTable.items():
    print(k, " :",len(v.inDict))

###Part 1: Normality test 
# a_car = firstTractorA.getDataPoins(finGp.element_of_group.CarNElement)
# h_car = firstTractorH.getDataPoins(finGp.element_of_group.CarNElement)


# res_a_car = stats.normaltest(a_car)
# res_a_car.statistic
# res_a_car.pvalue


# res_h_car = stats.normaltest(a_car)
# res_h_car.statistic
# res_h_car.pvalue

# ###Part 2: Normality test on the CarNews
# a_carNews = firstTractorA.getDataPoins(finGp.element_of_group.CarNewsElement)
# h_carNews = firstTractorH.getDataPoins(finGp.element_of_group.CarNewsElement)

# res_a_carNews = stats.normaltest(a_carNews)
# res_a_carNews.statistic
# res_a_carNews.pvalue


# res_h_carNews = stats.normaltest(a_carNews)
# res_h_carNews.statistic
# res_h_carNews.pvalue
