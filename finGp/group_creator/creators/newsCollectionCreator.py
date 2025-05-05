import csv

from ..creator import Creator
from ...date_utils import DateRepresentation
from ...element_of_group import NoneDataPoint,NewsDataPoint
from ...group import Group
from ...shareEntity import ShareEntity              
                

class NewsCollectionCreator(Creator): 
    _enum = ['date','siteAddress','sentimentalScore']

    @classmethod
    def getInstacnefrom(cls, fileName=str)->Group:
        return cls.getInstacnefromCsv(fileName)
    
    @classmethod
    def getInstacnefromCsv(cls, fileName=str,isHeading=True,shareCode='',dateIndex=0,siteAddressIndex=1,sentimentalScoreIndex=2)->Group:
        "fileName: a csv file with the date,siteAddress,sentimentalScore"
        collections = []
        with open(fileName,mode='r') as infile: 
            print(f"Reading {fileName}")
            reader = csv.reader(infile)         
            keyList = cls._getKeyList(dateIndex,siteAddressIndex,sentimentalScoreIndex)
            if isHeading:
                next(reader)
            for row in reader: 
                row_dict = dict(zip(keyList, row))
                date = row_dict.get(
                    cls._enum[0],
                    DateRepresentation.getNullInstance()
                )
                newsDataPoint = NewsDataPoint(
                    date,
                    row_dict.get(cls._enum[1],NoneDataPoint(date)),
                    row_dict.get(cls._enum[2],NoneDataPoint(date))
                )
                if newsDataPoint.valid():
                    collections.append(newsDataPoint)
                
        shareEntity = ShareEntity.createShareCode(shareCode)     
        return Group(shareEntity,NewsDataPoint.getGroupElement(collections))
    
    @classmethod
    def _getKeyList(cls,dateIndex:int,siteAddressIndex:int,sentimentalScoreIndex:int)->list: 
        keyList = [0]*3
        keyList[dateIndex] = cls._enum[0]
        keyList[siteAddressIndex] = cls._enum[1]
        keyList[sentimentalScoreIndex] = cls._enum[2]
        return keyList