from .dateRepresentation import DateRepresentation
from datetime import date

class AlwaysGreaterDateRepresentation(DateRepresentation): 

    def __init__(self):
        pass 

    def __lt__(self,other):
        return False 
        
    def __le__(self,other):
        return False       
    
           
    def __gt__(self,other):
        return True
    

    def __ge__(self,other):
        return True
    

    def __eq__(self,other): 
        return isinstance(other,AlwaysGreaterDateRepresentation)

    @property
    def standardFormat(self)->str:
        return '9999-01-01'
    
    @property
    def dateTimeDate(self)->date:
        return date(1,1,1)  
        
    def isSupmiumDay(self)->bool:
        return True 

    
    def changeToNextDay(self):
        pass     
    
    def changeToPreviousDay(self):
        pass 

    def changeToPrevious_N_Day(self):
        pass 
        
    def changeToNext_N_Day(self):
        pass 
    

    def createPrevious_N_Day(self,integer_N:int)->'DateRepresentation':
        return AlwaysGreaterDateRepresentation()            
    
    
    def createNext_N_Day(self,integer_N:int)->'DateRepresentation':
        return AlwaysGreaterDateRepresentation()         
 