from abc import ABC, abstractmethod
import datetime
import re 
from typing import Any, Callable



'''
make conversion between different date string format and datetime.date format 
standard format refer to yyyy-mm-dd
'''
class DateRepresentation(ABC): 
    _dateTypeFlag = ['string in standard format','datetime.date']        
    
    @abstractmethod
    def __lt__(self,other):
        pass 
    
    @abstractmethod
    def __le__(self,other):
        pass       
    
    @abstractmethod        
    def __gt__(self,other):
        pass 
    
    @abstractmethod
    def __ge__(self,other):
        pass 
    
    @abstractmethod
    def __eq__(self,other): 
        pass 


    @property
    @abstractmethod
    def standardFormat(self)->str:
        pass 
    
    @property
    @abstractmethod
    def dateTimeDate(self)->datetime.date:
        pass  

        
    @abstractmethod    
    def isSupmiumDay(self)->bool:
        pass 
    
    @abstractmethod
    def changeToNextDay(self):
        pass     
    
    @abstractmethod 
    def changeToPreviousDay(self):
        pass 

    @abstractmethod 
    def changeToPrevious_N_Day(self):
        pass 
        
    @abstractmethod 
    def changeToNext_N_Day(self):
        pass 
    

    @abstractmethod
    def createPrevious_N_Day(self,integer_N:int)->'DateRepresentation':
        pass            
    
    @abstractmethod
    def createNext_N_Day(self,integer_N:int)->'DateRepresentation':
        pass 


    @classmethod
    def getInstance(cls,dateObj):
        for subClasses in cls.__subclasses__():
            if subClasses.__name__ == 'DateRepresentationImp': 
                return subClasses(dateObj)
    
    @classmethod
    def getInstanceOfNullDate(cls): 
        for subClasses in cls.__subclasses__():
            if subClasses.__name__ == 'NullDateRepresentation': 
                return subClasses()

    @classmethod
    def getInstanceOfAlwaysGreaterDate(cls): 
        for subClasses in cls.__subclasses__():
            if subClasses.__name__ == 'AlwaysGreaterDateRepresentation': 
                return subClasses()            

        
        
    @staticmethod
    def toStandardFormat(dateObj)->str: 
        dateTypeFlag = DateRepresentation._determineDateType(dateObj)
        if dateTypeFlag == None:             
             raise InvalidDateType("Invalid Date Type")
        else:
            parsingFunction = DateRepresentation._getParsingFunctionToStandardFormat(dateTypeFlag)
            return parsingFunction(dateObj)              
    @staticmethod
    def toDateTimeDate(dateObj)->datetime.date:
        dateTypeFlag = DateRepresentation._determineDateType(dateObj)
        if dateTypeFlag == None:
            raise InvalidDateType("Invalid Date Type")
        else:
            parsingFunction = DateRepresentation._getParsingFunctionToDatetimeType(dateTypeFlag)
            return parsingFunction(dateObj)  
    #######################################     
    ### Start of Helper function for type conversion
    @staticmethod
    def _determineDateType(dateToBeDetermined)->str:
        if isinstance(dateToBeDetermined,str) and DateRepresentation.checkIfDateStandardFormat(dateToBeDetermined):
            return DateRepresentation._dateTypeFlag[0]
        elif isinstance(dateToBeDetermined,datetime.date):
            return DateRepresentation._dateTypeFlag[1]
        else: 
            return 'notInRange'                                        
    @staticmethod
    def _getParsingFunctionToDatetimeType(typeFlag)->Callable[[Any],datetime.date]: 
        '''return the appropriate function'''
        if typeFlag == DateRepresentation._dateTypeFlag[0]:
            return DateRepresentation._standardFormatToDateTime
        elif typeFlag == DateRepresentation._dateTypeFlag[1]:
            return DateRepresentation._dateTimeToDateTime
        else : 
            return None    
    @staticmethod
    def _getParsingFunctionToStandardFormat(typeFlag)->Callable[[Any],str]: 
        '''return the appropriate function'''
        if typeFlag == DateRepresentation._dateTypeFlag[0]:
            return DateRepresentation._standardFormatToStandardFormat
        elif typeFlag == DateRepresentation._dateTypeFlag[1]:
            return DateRepresentation._dateTimeToStandardFormat
        else : 
            return None  
              
    @staticmethod 
    def _standardFormatToDateTime(dateString:str)->datetime.date: 

        def extractYearFromStandardFormat(dateString:str)->int:
            dateInList=dateString.split('-')
            return int(dateInList[0])                    
        def extractMonthFromStandardFormat(dateString:str)->int:
            dateInList=dateString.split('-')
            return int(dateInList[1])                    
        def extractDayFromStandardFormat(dateString:str)->int:
            dateInList=dateString.split('-')
            return int(dateInList[2])     
                
        year = extractYearFromStandardFormat(dateString)
        month = extractMonthFromStandardFormat(dateString)
        day = extractDayFromStandardFormat(dateString)        
        
        return datetime.date(year,month,day)    
    @staticmethod
    def _dateTimeToDateTime(datetimeObj:datetime.date)->datetime.date:
        return datetimeObj
    @staticmethod 
    def _dateTimeToStandardFormat(dateInClass:datetime.date)->str: 
        yearString = dateInClass.year
        monthString = dateInClass.month
        dayString = dateInClass.day
        dateInStandardFormat = yearString+'-'+monthString+'-'+dayString
        return dateInStandardFormat    
    @staticmethod
    def _standardFormatToStandardFormat(datetimeStr:str)->str:
        return datetimeStr
    ### End of Helper function for type conversion        
    #######################################




    @staticmethod
    def getListOfDateStrWithinTwoDates(startedDateIncluded,endDateInclueded): 
        startD = DateRepresentation(startedDateIncluded)
        endD = DateRepresentation(endDateInclueded)
        dateList=[]
        while startD <= endD:
            dateList.append(startD.standardFormat)
            startD.changeToNextDay()
        return dateList        
        
    @staticmethod
    def checkIfDateStandardFormat(dateString)->bool:
        '''It checks if the string dateString is of 'yyyy-mm-dd' format    '''
        datePatten = r'\d{4}-\d{2}-\d{2}'
        return re.match(datePatten,dateString)      

    @staticmethod    
    def _raiseComparisonError():
        raise NotImplementedError("Comparison operators are not supported for NullDateRepresentation")        
               
    
    
    
    
    
class InvalidDateType(Exception):
    pass 
        
    
