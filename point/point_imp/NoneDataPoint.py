
from date_utils import DateRepresentation
from point.dataPoint import DataPoint

        
class NoneDataPoint(DataPoint): 
    '''
    A special class that represent the absent of market day 
    '''
    def __init__(self,date):
        self.__date = DateRepresentation(date)


    @property
    def date(self)->DateRepresentation: 
        return self.__date

    @property    
    def mapping(self):
        return {}
        
    def getValueWithAttribute(self, attribute):
        '''Expect it to pass an error'''        
        return self.mapping[attribute]    

    @property
    def coordinate(self):
        '''Special Index saved for NoneDataPoint'''
        return 'NoneDataPoint'+self.date.dateTimeDate
    
    def valid():  
        return False                       
    
    @classmethod
    def getCoordinateFrom(cls):
        return ''
    
    @classmethod
    def equivalent(cls):
        return False
    
