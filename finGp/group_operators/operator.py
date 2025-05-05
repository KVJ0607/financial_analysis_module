from __future__ import annotations

from abc import ABC, abstractmethod





class CollectionOperator(ABC) :     
    """ 
    Handle binary opertaion between object of DataCollection with the 
    different pointType attribute.The actual logic depends on the pointType attribute 
    from both operand.
        
    A class that provide classmethods that acts as operators between dataCollections 
    having different pointType attribute.
    """
    
    @property
    @abstractmethod
    def productClass(self):
        pass 
        
        
    @classmethod
    @abstractmethod
    def match(
        cls,
        classA,
        classB)->bool: 
        """
        Check if the two DataCollection are compatible 
        for the operator. 
        """
        pass


    @classmethod
    @abstractmethod
    def dot(
        cls,
        leftOperand,
        rightOperand):
        """
        The dot method is a classmethod that acts as a
        operator of Element. It will return a new
        Element.
        """
        pass
    
    @classmethod
    @abstractmethod
    def signatures(cls)->list[set]: 
        """Return a list of set which act as a signature.
        Each signature is a set of two type[Element] which
        can be the operant.
        """        
        pass 
    
    @classmethod 
    def getOperator(
        cls,
        targetClass)->type[CollectionOperator]:
        for subclass in cls.__subclasses__():
            if targetClass == subclass.productClass:
                return subclass
