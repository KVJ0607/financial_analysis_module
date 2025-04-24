from ....date_utils.dateRepresentation import DateRepresentation
from ..data_point import DataPoint

        
class NoneDataPoint(DataPoint): 
    '''
    A special class that represent the absent of market day 
    '''
    def __init__(self,date):
        self.__date = DateRepresentation.getInstance(date)


    @property
    def date(self)->DateRepresentation: 
        return self.__date

    @property    
    def mapping(self):
        return {}
        
    def getDataValueWithAttribute(self, attribute):
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
    def comparable(cls):
        return False
    
