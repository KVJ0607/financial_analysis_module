from abc import ABC,abstractmethod
import csv
from date_utils import DateRepresentation
from point import NoneDataPoint,PricingDataPoint,NewsNewsDataPoint
from collectionGroup import CollectionGroup
from shareEntity import ShareEntity

class Creator(ABC): 
    
    @classmethod
    @abstractmethod
    def getInstacnefrom(cls,fileName=str)->CollectionGroup:
        pass 
        