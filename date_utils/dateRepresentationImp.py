import datetime

from ..date_utils.dateRepresentation import DateRepresentation
from ..date_utils.nullDateRepresentation import NullDateRepresentation





'''
make conversion between different date string format and datetime.date format 
standard format refer to yyyy-mm-dd
'''
class DateRepresentationImp(DateRepresentation): 
    _dateTypeFlag = ['string in standard format','datetime.date']
    
    def __init__(self,dateObj):                
        self.__dateStringInStandardFormat = DateRepresentation.toStandardFormat(dateObj)
        self.__dateTimeDate = DateRepresentation.toDateTimeDate(dateObj)
        self.__isSupmiumDay = False #A flag that indicte this is a always greater than elements except for element with true flag

        
    @property
    def standardFormat(self)->str:
        return self.__dateStringInStandardFormat    
        
    @property
    def dateTimeDate(self)->datetime.date:
        return self.__dateTimeDate  
    
                 
    '''
    Comparasion Logic
    Let a,b be ordinary day, X and Y be supmiumDay
    a<X true 
    a>X false 
    a==X false 
    X<Y false
    X==Y false        
    '''
    def __lt__(self,other:'DateRepresentationImp'):
        DateRepresentationImp._errorHandlingIfContainNullDate(DateRepresentation._raiseComparisonError,self,other)
        if DateRepresentationImp._checkIfEitherIsSupmiumDay(self,other):
            return False
        else : 
            return self.dateTimeDate < other.dateTimeDate    
        
    def __le__(self,other:'DateRepresentationImp'):
        DateRepresentationImp._errorHandlingIfContainNullDate(DateRepresentation._raiseComparisonError,self,other)        
        if DateRepresentationImp._checkIfEitherIsSupmiumDay(self,other):            
            return False
        else: 
            return self.dateTimeDate <= other.dateTimeDate                       
        
    def __gt__(self,other:'DateRepresentationImp'):        
        DateRepresentationImp._errorHandlingIfContainNullDate(DateRepresentation._raiseComparisonError,self,other)
        if DateRepresentationImp._checkIfEitherIsSupmiumDay(self,other):            
            return False
        else: 
            return self.dateTimeDate > other.dateTimeDate    
        
    def __ge__(self,other:'DateRepresentationImp'):
        DateRepresentationImp._errorHandlingIfContainNullDate(DateRepresentation._raiseComparisonError,self,other)        
        if DateRepresentationImp._checkIfEitherIsSupmiumDay(self,other):
            return False  
        else: 
            return self.dateTimeDate >= other.dateTimeDate    
        
    def __eq__(self,other:'DateRepresentationImp'):         
        DateRepresentationImp._errorHandlingIfContainNullDate(DateRepresentation._raiseComparisonError,self,other)
        if DateRepresentationImp._checkIfEitherIsSupmiumDay(self,other):
            return False 
        else : 
            return self.dateTimeDate == other.dateTimeDate
        
    @staticmethod
    def _checkIfEitherIsSupmiumDay(thisDay:'DateRepresentationImp',thatDay:'DateRepresentationImp'):      
        return thisDay.isSupmiumDay() or thatDay.isSupmiumDay()

    @staticmethod
    def _errorHandlingIfContainNullDate(errorFunction,*arg): 
        for element in list(arg): 
            if isinstance(element,NullDateRepresentation): 
                errorFunction()

    
        
    def isSupmiumDay(self)->bool:
        return self.__isSupmiumDay
    
    def changeToNextDay(self):
        self.changeToNext_N_Day(1)                        

    def changeToPreviousDay(self):
        self.changeToNext_N_Day(-1)                        
        
    def changeToPrevious_N_Day(self,nDay):
        self.changeToNext_N_Day(-nDay)

    def changeToNext_N_Day(self,nDay):
        mToday = self.dateTimeDate
        mNewDay = mToday + datetime.timedelta(days=int(nDay))
        self.dateTimeDate = mNewDay
        self.__dateStringInStandardFormat = DateRepresentationImp.toStandardFormat(mNewDay)                


    def createPrevious_N_Day(self,integer_N:int):
        return self.createNext_N_Day(-integer_N) 
               
    def createNext_N_Day(self,integer_N:int):
        return self.dateTimeDate + datetime.timedelta(days=integer_N) 

    

    
    
    
    
    
    
    
        
        
    
