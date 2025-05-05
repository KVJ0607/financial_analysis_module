import csv

from ..creator import Creator
from ...date_utils import DateRepresentation
from ...element_of_group import NoneDataPoint,PricingDataPoint
from ...group import Group
from ...shareEntity import ShareEntity


class PricingCollectionCreator(Creator): 
    _enum = ['date','open','high','low','close','adjClose','volume']
    
    
    @classmethod
    def getInstacnefrom(cls, fileName=str)->Group:
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
        return Group(shareEntity,PricingDataPoint.getGroupElement(collections))

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
                
                    