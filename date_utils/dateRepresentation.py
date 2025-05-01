import datetime
import re 
from typing import Callable,Any





'''
make conversion between different date string format and datetime.date format 
standard format refer to yyyy-mm-dd
'''
class DateRepresentation: 
    _dateTypeFlag = ['string in standard format','datetime.date','DateRepresentation']
    
    def __init__(self,dateGeneric,nullDay:bool=False):     
        
        if nullDay:
            self.__dateTimeDate = datetime.date(1,1,1)
            self.__nullDay = True
            return
        
        try:           
            self.dateTimeDate = dateGeneric
            self.__nullDay = False
        except InvalidDateType as e:
            self.__dateTimeDate = datetime.date(1,1,1)
            self.__nullDay = True
                
    @property
    def dateTimeDate(self)->datetime.date:
        return self.__dateTimeDate  
    
    @dateTimeDate.setter
    def dateTimeDate(self,dateGeneric):
        self.__dateTimeDate = self.toDateTimeDate(dateGeneric)        
    
    @property
    def isNullDay(self)->bool:
        return self.__nullDay    
    

    @property
    def standardFormat(self)->str:        
        return self._dateTimeToStandardFormat(self.__dateTimeDate)
    
    @property
    def year(self)->int:
        return self.dateTimeDate.year
    @property
    def month(self)->int:
        return self.dateTimeDate.month
    @property
    def day(self)->int:
        return self.dateTimeDate.day

        
    def __add__(self, o:int):
        if self.isNullDay: 
            return self.getNullInstance()
        return self.createNext_N_Day(o)    
    def __sub__(self, o:int):
        if self.isNullDay: 
            return self.getNullInstance()
        return self.createPrevious_N_Day(o)           
    def __hash__(self):
        return self.year*10000 + self.month*100 + self.day    
    
    def __str__(self):
        if self.isNullDay: 
            return 'Null Day'
        else:
            return self.standardFormat
    
    def __lt__(self,other:'DateRepresentation'):
        if self.isNullDay or other.isNullDay: 
            raise
        return self.dateTimeDate < other.dateTimeDate    
        
    def __le__(self,other:'DateRepresentation'):
        if self.isNullDay or other.isNullDay: 
            raise     
        else: 
            return self.dateTimeDate <= other.dateTimeDate                       
        
    def __gt__(self,other:'DateRepresentation'):        
        if self.isNullDay or other.isNullDay: 
            raise
        return self.dateTimeDate > other.dateTimeDate    
        
    def __ge__(self,other:'DateRepresentation'):
        if self.isNullDay or other.isNullDay: 
            raise
        return self.dateTimeDate >= other.dateTimeDate    
        
    def __eq__(self,other:'DateRepresentation'):         
        if self.isNullDay or other.isNullDay: 
            raise
        return self.dateTimeDate == other.dateTimeDate
        

    @classmethod
    def getNullInstance(cls)->'DateRepresentation':
        return cls(datetime.date(1,1,1),True)    

    
    def changeToNextDay(self):
        self.changeToNext_N_Day(1)                        

    def changeToPreviousDay(self):
        self.changeToNext_N_Day(-1)                        
        
    def changeToPrevious_N_Day(self,nDay):
        self.changeToNext_N_Day(-nDay)

    def changeToNext_N_Day(self,nDay):
        if self.isNullDay:
            pass 
        else:
            mToday = self.dateTimeDate
            mNewDay = mToday + datetime.timedelta(days=int(nDay))
            self.__dateTimeDate = mNewDay            


    def createPrevious_N_Day(self,integer_N:int):
        return self.createNext_N_Day(-integer_N) 
               
    def createNext_N_Day(self,integer_N:int)->'DateRepresentation':
        if self.isNullDay:
            return self.getNullInstance()
        return DateRepresentation(self.dateTimeDate + datetime.timedelta(days=integer_N))


    
    @classmethod
    def getDateRange(cls,startedDateIncluded,endDateInclueded)->list['DateRepresentation']:  
        dateList = cls.getDateRangeInStr(startedDateIncluded, endDateInclueded)        
        for i in range(len(dateList)):
            dateList[i] = cls(dateList[i])                
        return dateList

    @classmethod
    def getDateRangeInStr(cls, startedDateIncluded, endDateInclueded)->list[str]:
        startD = cls(startedDateIncluded)
        endD = cls(endDateInclueded)   
        dateList=[]
        while startD <= endD:                        
            dateList.append(startD.standardFormat)
            startD.changeToNextDay()
        return dateList
        
    @classmethod
    def isValid(cls,dateObj): 
        if isinstance(dateObj,cls):
            return True
        elif isinstance(dateObj,str) and cls.checkIfDateStandardFormat(dateObj):
            return True
        elif isinstance(dateObj,datetime.date):
            return True
        else:
            return False
    @staticmethod
    def checkIfDateStandardFormat(dateString)->bool:
        '''It checks if the string dateString is of 'yyyy-mm-dd' format    '''
        datePatten = r'\d{4}-(?:\d{2}|\d{1})-(?:\d{2}|\d{1})'
        return re.match(datePatten,dateString) 

    @staticmethod    
    def _raiseComparisonError():
        raise NotImplementedError("Comparison operators are not supported for NullDateRepresentation")        

        
    @classmethod
    def toStandardFormat(cls,dateObj)->str: 
        dateTypeFlag = cls._determineDateType(dateObj)
        if dateTypeFlag == None:             
             raise InvalidDateType("Invalid Date Type")
        else:
            parsingFunction = cls._getParsingFunctionToStandardFormat(dateTypeFlag)
            return parsingFunction(dateObj)              
        
    @classmethod
    def toDateTimeDate(cls,dateObj)->datetime.date:
        dateTypeFlag = cls._determineDateType(dateObj)
        if dateTypeFlag == None:
            raise InvalidDateType(f"Invalid Date Type {dateObj}")
        else:
            parsingFunction = cls._getParsingFunctionToDatetimeType(dateTypeFlag)
            return parsingFunction(dateObj)          
        
    #######################################     
    ### Start of Helper function for type conversion
    @classmethod
    def _determineDateType(cls,dateToBeDetermined)->str:
        if isinstance(dateToBeDetermined,DateRepresentation):
            return cls._dateTypeFlag[2]
        elif isinstance(dateToBeDetermined,str) and DateRepresentation.checkIfDateStandardFormat(dateToBeDetermined):
            return cls._dateTypeFlag[0]
        elif isinstance(dateToBeDetermined,datetime.date):
            return cls._dateTypeFlag[1]
        else: 
            return None                                        
        
    @classmethod
    def _getParsingFunctionToDatetimeType(cls,typeFlag)->Callable[[Any],datetime.date]: 
        '''return the appropriate function'''
        if typeFlag == cls._dateTypeFlag[0]:
            return cls._standardFormatToDateTime
        elif typeFlag == cls._dateTypeFlag[1]:
            return cls._dateTimeToDateTime
        elif typeFlag == cls._dateTypeFlag[2]:
            return cls._dateRepresentationToDateTime
        else : 
            return None    
    @classmethod
    def _getParsingFunctionToStandardFormat(cls,typeFlag)->Callable[[Any],str]: 
        '''return the appropriate function'''
        if typeFlag == cls._dateTypeFlag[0]:
            return cls._standardFormatToStandardFormat
        elif typeFlag == cls._dateTypeFlag[1]:
            return cls._dateTimeToStandardFormat
        elif typeFlag == cls._dateTypeFlag[2]:
            return cls._dateRepresentationToStandardFormat
        else : 
            return None  
              
    @staticmethod 
    def _standardFormatToDateTime(dateString:str)->datetime.date: 
        def removeLeadingZero(dateString:str)->str:
            if dateString[0] == '0':
                return dateString[1:]
            else: 
                return dateString
        def extractYearFromStandardFormat(dateString:str)->int:
            dateInList=dateString.split('-')
            
            
            return int(removeLeadingZero(dateInList[0]))                    
        def extractMonthFromStandardFormat(dateString:str)->int:
            dateInList=dateString.split('-')
            return int(removeLeadingZero(dateInList[1]))                    
        def extractDayFromStandardFormat(dateString:str)->int:
            dateInList=dateString.split('-')
            return int(removeLeadingZero(dateInList[2]))     
                
        year = extractYearFromStandardFormat(dateString)
        month = extractMonthFromStandardFormat(dateString)
        day = extractDayFromStandardFormat(dateString)        
        
        return datetime.date(year,month,day)    
    
    @classmethod
    def _dateRepresentationToDateTime(cls,dateObj:'DateRepresentation')->datetime.date:
        return dateObj.dateTimeDate
    
    @classmethod
    def _dateRepresentationToStandardFormat(cls,dateObj:'DateRepresentation')->str:
        return dateObj.standardFormat
    @staticmethod
    def _dateTimeToDateTime(datetimeObj:datetime.date)->datetime.date:
        return datetimeObj
    @staticmethod 
    def _dateTimeToStandardFormat(dateInClass:datetime.date)->str: 
        yearString = str(dateInClass.year)
        monthString = str(dateInClass.month)
        dayString = str(dateInClass.day)
        if len(monthString) == 1:
            monthString = '0'+monthString
        if len(dayString) == 1:
            dayString = '0'+dayString
        dateInStandardFormat = yearString+'-'+monthString+'-'+dayString
        return dateInStandardFormat    
    @staticmethod
    def _standardFormatToStandardFormat(datetimeStr:str)->str:
        return datetimeStr
    ### End of Helper function for type conversion        
    #######################################

    
class InvalidDateType(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return f'{self.message}'
        