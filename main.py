from creator import PricingCollectionCreator,NewsCollectionCreator
from financial_analysis import CollectionGroup

firstTractorH = PricingCollectionCreator.getInstacnefrom("example_data/hshare/0038.HK.csv")
firstTractorA = PricingCollectionCreator.getInstacnefrom("example_data/ashare/601038.SH.csv")
newsSentiment = NewsCollectionCreator.getInstacnefrom("example_data/sentiment/test_data.csv")


firstTractorA.joinGroupTable(newsSentiment)
firstTractorH.joinGroupTable(newsSentiment)


