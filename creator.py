"""
    Creator class handle the creation of DataCollection from source files or json like data of mutiple data point
"""


from abc import ABC,abstractmethod
import csv
from date_utils import DateRepresentation
from point import NoneDataPoint,PricingDataPoint,NewsNewsDataPoint
from financial_analysis.dataCollection import CollectionGroup
from shareEntity import ShareEntity

class Creator(ABC): 
    
    @classmethod
    @abstractmethod
    def getInstacnefrom(cls,fileName=str)->CollectionGroup:
        pass 
        
    

class PricingCollectionCreator(Creator): 
    _enum = ['date','open','high','low','close','adjClose','volume']
    
    
    @classmethod
    def getInstacnefrom(cls, fileName=str)->CollectionGroup:
        return cls.getInstacnefromCsv(fileName)
    
    @classmethod
    def getInstacnefromCsv(cls,fileName=str,isHeading=True,shareCode='',dateIndex=0,
                           openIndex=1,highIndex=2,lowIndex=3,closeIndex=4,
                           AdjCloseIndex=5,volumnIndex=6):
        "fileName: a csv file with the date,open,high,low,close,adjClose,volume"
        collections = []
        with open(fileName,mode='r') as infile: 
            print(f"Reading {fileName}")
            reader = csv.reader(infile)         
            keyList = cls._getKeyList(dateIndex,openIndex,highIndex,lowIndex,closeIndex,AdjCloseIndex,volumnIndex)
            if isHeading:
                next(reader)
            for row in reader: 
                row_dict = dict(zip(keyList, row))
                date = row_dict.get(cls._enum[0],DateRepresentation.getNullInstance())
                
                newDataPoint = PricingDataPoint(
                    date,
                    row_dict.get(cls._enum[1], NoneDataPoint(date)),
                    row_dict.get(cls._enum[2], NoneDataPoint(date)),
                    row_dict.get(cls._enum[3], NoneDataPoint(date)),
                    row_dict.get(cls._enum[4], NoneDataPoint(date)),
                    row_dict.get(cls._enum[5], NoneDataPoint(date)),
                    row_dict.get(cls._enum[6], NoneDataPoint(date))
                )
                
                if newDataPoint.valid():
                    collections.append(newDataPoint)
                                   
        shareEntity = ShareEntity.createShareCode(shareCode)
        return CollectionGroup(collections,shareEntity)

    @classmethod
    def _getKeyList(cls,dateIndex,openIndex,highIndex,lowIndex,closeIndex,AdjCloseIndex,volumnIndex)->list[str]:
        keyList =['']*7
        keyList[dateIndex] = cls._enum[0]
        keyList[openIndex] = cls._enum[1]
        keyList[highIndex] = cls._enum[2]
        keyList[lowIndex] = cls._enum[3]
        keyList[closeIndex] = cls._enum[4]
        keyList[AdjCloseIndex] = cls._enum[5]
        keyList[volumnIndex] = cls._enum[6]
        return keyList
                
                    
                
                

class NewsCollectionCreator(Creator): 
    _enum = ['date','siteAddress','sentimentalScore']

    @classmethod
    def getInstacnefrom(cls, fileName=str)->CollectionGroup:
        return cls.getInstacnefromCsv(fileName)
    
    @classmethod
    def getInstacnefromCsv(cls, fileName=str,isHeading=True,shareCode='',dateIndex=0,siteAddressIndex=1,sentimentalScoreIndex=2)->NewsNewsDataPoint:
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
                newDataPoint = NewsNewsDataPoint(
                    date,
                    row_dict.get(cls._enum[1],NoneDataPoint(date)),
                    row_dict.get(cls._enum[2],NoneDataPoint(date))
                )
                if newDataPoint.valid():
                    collections.append(newDataPoint)
                
        shareEntity = ShareEntity.createShareCode(shareCode)     
        return CollectionGroup(collections,shareEntity)
    
    @classmethod
    def _getKeyList(cls,dateIndex:int,siteAddressIndex:int,sentimentalScoreIndex:int)->list: 
        keyList = [0]*3
        keyList[dateIndex] = cls._enum[0]
        keyList[siteAddressIndex] = cls._enum[1]
        keyList[sentimentalScoreIndex] = cls._enum[2]
        return keyList