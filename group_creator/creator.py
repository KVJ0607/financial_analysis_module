from abc import ABC,abstractmethod
import csv
from date_utils import DateRepresentation
from point import NoneDataPoint,PricingDataPoint,NewsNewsDataPoint
from group import Group
from shareEntity import ShareEntity

class Creator(ABC): 
    
    @classmethod
    @abstractmethod
    def getInstacnefrom(cls,fileName=str)->Group:
        pass 
        