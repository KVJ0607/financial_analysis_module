import finGp
from scipy import stats


finGp.Space.initDefaultSpaceDefinition()
firstTractorH = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/hshare/0038.HK.csv",shareCode='0038.HK')
firstTractorA = finGp.creator.PricingCollectionCreator.getInstacnefromCsv("example_data/ashare/601038.SH.csv",shareCode='601038.SH')
newsSentiment = finGp.creator.NewsCollectionCreator.getInstacnefromCsv("example_data/sentiment/test_data.csv",shareCode='0038.HK')


firstTractorA.joinGroupTable(newsSentiment)
firstTractorH.joinGroupTable(newsSentiment)

firstTractorA.update()
firstTractorH.update()


firstTractorA.acceptOutVisitor("output/firstTractorA_withoutN.csv")
firstTractorH.acceptOutVisitor("output/firstTractorH_withoutN.csv")

finGp.Group.normalizeAllGroups(firstTractorA,firstTractorH)


firstTractorA.acceptOutVisitor("output/firstTractorA")
firstTractorH.acceptOutVisitor("output/firstTractorH")





