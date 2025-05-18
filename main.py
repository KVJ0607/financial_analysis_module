import copy

import finGp

from scipy import stats

firstTractorH = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/hshare/0038.HK.csv",shareCode='0038.HK')
firstTractorA = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/ashare/601038.SH.csv",shareCode='601038.SH')
newsSentiment = finGp.creator.NewsCollectionCreator.getInstacnefromCsv("example_data/sentiment/test_data.csv",shareCode='0038.HK')


firstTractorA.joinGroupTable(newsSentiment)
firstTractorH.joinGroupTable(newsSentiment)
    


finGp.Group.normalizeAllGroups(firstTractorA,firstTractorH)









#Part 1: Normality test 

##List of Car
aCar = firstTractorA.getElement(finGp.element.CarNElement(interval=3))
hCar = firstTractorH.getElement(finGp.element.CarNElement(interval=3))




##List of CarNews DataPoint
aCarNew = firstTractorA.getElement(finGp.element.CarNewsElement)
hCarNew = firstTractorH.getElement(finGp.element.CarNewsElement)


    

         
    

resACar = stats.normaltest(aCar)
print("aCar pValue:",resACar.pvalue)

resHCar = stats.normaltest(hCar)
print("hCar pValue:",resHCar.pvalue)




