from abc import ABC,abstractmethod
from typing import Type

from ..date_utils import DateRepresentation
from .. import DataCollection,DataPoint,CarNDataPoint,NoneDataPoint,NewsNewsDataPoint,HistoricalDataPoint





class HeterogCollectionOperator(ABC) :     
    """ 
    Handle binary opertaion between object of DataCollection with the 
    different pointType attribute.The actual logic depends on the pointType attribute 
    from both operand.
        
    A class that provide classmethods that acts as operators between dataCollections 
    having different pointType attribute.
    """
    
    __leftOperand = NoneDataPoint
    __rightOperand = NoneDataPoint
    
    @classmethod
    @abstractmethod
    def needNewWindow(cls)->bool: 
        pass
    
    @classmethod
    @abstractmethod
    def signature(cls)->set: 
        pass
    
    @classmethod
    @abstractmethod
    def interact(
        cls,operandA:DataCollection,
        operandB:DataCollection)->DataCollection: 
        """
        Interact the two DataCollection according 
        to the logic for their point type.
        
        """        
        pass 
        
    @classmethod
    @abstractmethod
    def createNewWindow(
            cls,operandA:DataCollection,
            operandB:DataCollection)->DataCollection: 
        """
        output a new DataCollection using a function 
        according to their point type.
        
        """
        pass 
    
    

    
    @classmethod
    def __getLeftOperandPointType(cls)->Type[DataPoint]: 
        '''
        Built to meet the non-communcative property.
        Raise error if not implemented
        '''        
        raise NotImplementedError ("left operand is not implemented")
        
    
    @classmethod
    def __getRightOperandPointType(cls)->Type[DataPoint]:  
        '''
        Built to meet the non-communcative property.
        Raise error if not implemented
        '''        
        raise NotImplementedError ("right operand is not implemented")
        
    
    @classmethod
    def __matchingOperand(cls,
                        leftInputCollection:DataCollection,
                        rightInputCollection:DataCollection)->tuple[DataCollection]: 
        """
        All opertors are implictly non-communicative and are only defined for 
        a specified ordered. This method take two operands and return 
        them in a required oreder in a tuple.      
        """
        leftOperandType = cls.__getLeftOperandPointType()
        rightOperandType = cls.__getRightOperandPointType()
        leftInputType = leftInputCollection.pointType
        rightInputType = leftInputCollection.pointType
        
        if leftInputType == leftOperandType and rightInputType == rightOperandType: 
            return leftInputCollection,rightInputCollection
        elif rightInputType == leftOperandType and leftInputType == rightOperandType: 
            return rightInputCollection,leftInputCollection
        else: 
            raise TypeError(f'''The two input should be of types {leftOperandType} and {rightOperandType}.
                            However, the arugments are of types {leftInputType} and {rightInputType}''')
    
class CarNewsOperators(HeterogCollectionOperator): 
    """
    A class that provide a classmethod that acts as a operator between dataCollections 
    with cars and news data points.

    
    """
    __leftOperand = CarNDataPoint 
    __rightOperand = NewsNewsDataPoint
    
    @classmethod
    def needNewWindow(cls)->bool: 
        return True
    
    @classmethod
    def signature(cls)->set: 
        return set([CarNDataPoint.__name__,NewsNewsDataPoint.__name__])          
    
    @classmethod
    def interact(cls): 
        pass 
    
    @classmethod
    def createNewWindow(cls, leftOperand:DataCollection,
             rightOperand:DataCollection) -> DataCollection:
        carCollection: DataCollection
        newsCollection: DataCollection
        
        carCollection,newsCollection = cls.__matchingOperand(leftOperand,rightOperand)        
        
        carNewsDataPoints = []
        
        for carCoordinate,carPoint in carCollection.dataPoints: 
            carCoordinate:str
            carPoint:CarNDataPoint
            
            previousDate = carPoint.previousDate
            followingDate = carPoint.followingDate
            carDate = carPoint.date
                 
            accumlatedSentimentalScore = 0                    
            for iTime in DateRepresentation.getListOfDateStrWithinTwoDates(previousDate,followingDate): 
                iDataPoint = newsCollection.getDataPointFromCoordinate(NewsNewsDataPoint.getCoordinateFrom(iTime))
                accumlatedSentimentalScore += iDataPoint.getDataValueWithAttribute(NewsNewsDataPoint.enum()[1])
                
            attriList = ['sentimentalScore']                
            carNewsDataPoints.append(HistoricalDataPoint(carDate,attriList,[accumlatedSentimentalScore],attriList))
        
        return DataCollection(carNewsDataPoints,carCollection.shareEntity)     
            
        
        
