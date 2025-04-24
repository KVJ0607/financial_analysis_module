import re
from abc import ABC,abstractmethod


class ShareEntity(ABC):
    '''
    Act as an interface and a factory
    Each subclass of ShareCode represent a share market region. 
    It provide ways to create and report error of share code, store its region information
    '''    

    class MarketRegion:     
        def __init__(self,name): 
            self.name = name
        
        def __str__(self): 
            return str(self.name)
        
        def getRegionName(self):
            return self.name
    
    class NoneRegion(MarketRegion): 
        def __init__(self): 
            self.__NoneRegion = True 
            
        def __str__(self): 
            return ''
        
        def getRegionName(self):
            return ''        
        
    @property
    @abstractmethod
    def isolatedNumericalCode(self)->str:
        pass 
    
    @property
    @abstractmethod
    def isolatedMarketCode(self)->str: 
        pass 
    
    @property
    @abstractmethod
    def shareCode(self)->str:
        pass    
    
    @property
    @abstractmethod
    def region(self)->MarketRegion:
        pass 

    
    @classmethod
    def createShareCode(cls,shareCode) ->'ShareEntity': 
        if isinstance(shareCode,ShareEntity): 
            return shareCode
        for mSubclass in ShareEntity.__subclasses__(): 
            if mSubclass.validableCode(shareCode): 
                return mSubclass(shareCode)
        raise Exception("Invaild share code: "+shareCode)         
    
    @classmethod
    def createJoinedShareCode(cls,*args) ->'ShareEntity': 
        shareCodes = list(args)
                
        joinedEntities = []
        for i_code in shareCodes: 
            joinedEntities.append(cls.createShareCode(i_code))
            
        return JoinedShareEntity(joinedEntities)
        
    @abstractmethod                        
    @classmethod
    def validableCode(cls,inputStr)->bool:
        pass
    
    @abstractmethod
    @classmethod
    def validifyCode(cls,inputStr)->str: 
        pass 
                             

class NoneEntity(ShareEntity):
    '''
    Act as an interface and a factory
    Each subclass of ShareCode represent a share market region. 
    It provide ways to create and report error of share code, store its region information
    '''    
    def __init__(self,shareCode):
        self.__code = ''
    
    @property
    def isolatedNumericalCode(self)->str:
        return '' 
    
    @property
    def isolatedMarketCode(self)->str: 
        return '' 
    
    @property
    def shareCode(self)->str:
        return ''    
    
    @property    
    def region(self)->ShareEntity.NoneRegion:
        return ShareEntity.NoneRegion() 

    
    @classmethod
    def createShareCode(cls,shareCode) ->'ShareEntity': 
        return NoneEntity()
    
    
    @classmethod
    def validableCode(cls,inputStr:str)->bool:
        if inputStr=='': 
            return True
        else: 
            return False
    
    @classmethod
    def validifyCode(cls)->str: 
        return '' 
                           


class H_ShareEntity(ShareEntity): 
    '''Market code in Hong Kong'''
    
    def __init__(self,hCode): 
        '''
        e.g. 03678.HK,5digit number + .HK
        numbericalCode = 03678, marketCode = .HK (upper Case)         
        '''           
        def createNumericalCode(hCode:str):   
            hCode = hCode.strip()      
            if H_ShareEntity.validableCode():
                hCode = H_ShareEntity.validifyCode(hCode)
                return hCode.split('.')[0]
            else: 
                raise Exception("This is not a valid H-share market Code: "+hCode)     
        
        def createMarketCode(hCode:str): 
            if H_ShareEntity.validableCode(): 
                return '.'+hCode.split('.')[1].upper()
            else: 
                raise Exception("This is not a valid H-share market Code: "+hCode)    
                     
        self.isolatedNumericalCode=createNumericalCode(hCode)
        self.isolatedMarketCode=createMarketCode(hCode)
        self.shareCode = self.isolatedNumericalCode +'.'+self.isolatedMarketCode
        self.region = super().MarketRegion('Hong Kong')          
    
    
                        
    @classmethod
    def validableCode(cls,inputStr:str)->bool:
        '''
        Check if it is valid or can be added a single prefix '0' to be it valid
        e.g. 12345.HK valid, 2345.HK can be transformed to 02345.HK 
        '''
        inputStr = inputStr.strip()
        patternOne = r'^\d{5}\.(hk|HK)$'
        patternTwo = r'^\d{4}\.(hk|HK)$'
        if re.match(patternOne, inputStr) or re.match(patternTwo,inputStr):
            return True
        else:
            return False 
                   
    @classmethod
    def validifyCode(cls,inputStr:str)->str: 
        inputStr = inputStr.strip()
        patternOne = r'^\d{5}\.(hk|HK)$'
        patternTwo = r'^\d{4}\.(hk|HK)$'        
        if re.match(patternOne, inputStr):
            return inputStr
        elif re.match(patternTwo,inputStr):
            return '0'+inputStr
        else: 
            raise Exception('This code is not valid: '+inputStr)
            
    
class A_ShareEntity(ShareEntity): 
    '''market code in China'''    

    def __init__(self,aCode): 
        '''
        e.g. 601288.SS or 123456.SZ
        numbericalCode = 601288 or 123456 , marketCode = .SS or .SZ(upper Case)         
        '''
        def createNumericalCode(aCode:str): 
            if A_ShareEntity.validableCode(aCode):             
                aCode = A_ShareEntity.validifyCode(aCode)
                return aCode.split('.')[0]
            else: 
                raise Exception("This is not a valid A-share market Code: "+aCode)             
        def createMarketCode(aCode:str): 
            if A_ShareEntity.validableCode(): 
                aCode = A_ShareEntity.validifyCode(aCode) 
                return '.'+aCode.split('.')[1].upper()
            else: 
                raise Exception("This is not a valid A-share market Code: "+aCode)  
                    
        self.isolatedNumericalCode=createNumericalCode(aCode)
        self.isolatedMarketCode=createMarketCode(aCode)      
        self.shareCode = self.isolatedNumericalCode +'.'+self.isolatedMarketCode 
        self.region = super().MarketRegion('China')  
        
    

    @staticmethod
    def validableCode(input_str:str)->bool:
        '''
        Check if it is valid or can be added a single prefix '0' to be it valid
        e.g. 688347.SS valid, 88347.SS can be transformed to 088347.SS
        '''      
        inputStr = inputStr.strip()
        patternOne = r'^\d{6}\.(ss|SS|sz|SZ)$'
        patternTwo = r'^\d{5}\.(ss|SS|sz|SZ)$'
        if re.match(patternOne, input_str) or re.match(patternTwo, input_str):
            return True
        else:
            return False      
           
    @staticmethod    
    def validifyCode(inputStr:str)->str: 
        inputStr = inputStr.strip()
        patternOne = r'^\d{6}\.(ss|SS|sz|SZ)$'
        patternTwo = r'^\d{5}\.(ss|SS|sz|SZ)$'       
        if re.match(patternOne, inputStr):
            return inputStr
        elif re.match(patternTwo,inputStr):
            return '0'+inputStr
        else: 
            raise Exception('This code is not valid: '+inputStr)


class JoinedShareEntity(ShareEntity):
     
    def __init__(self,joinedEntities:list[ShareEntity]):
        self.joinedEntities = joinedEntities
         
    @property    
    def isolatedNumericalCode(self)->list[str]:
        isoCodes = []
        for entity in self.joinedEntities: 
            isoCodes.append(entity.isolatedNumericalCode)
        return isoCodes
    
    @property
    def isolatedMarketCode(self)->list[str]: 
        isoCodes = []
        for entity in self.joinedEntities: 
            isoCodes.append(entity.isolatedMarketCode)
        return isoCodes         
    
    @property
    def shareCode(self)->list[str]:
        isoCodes = []
        for entity in self.joinedEntities: 
            isoCodes.append(entity.shareCode)
        return isoCodes      
    
    @property
    def region(self)->list[ShareEntity.MarketRegion]:
        regions = []
        for entity in self.joinedEntities: 
            regions.append(entity.region)
        return regions
                              
    @classmethod
    def validableCode(cls,inputStr)->bool:
        return False
    
    @classmethod
    def validifyCode(cls,inputStr)->str: 
        return '' 
                       
class clsMethodNotImplemented(Exception):
    def __init__(self, message='The method is not implemented'):
        self.message=message
        
        