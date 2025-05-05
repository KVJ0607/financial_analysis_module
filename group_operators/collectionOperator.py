from __future__ import annotations

from abc import ABC, abstractmethod
from element_of_group import Element





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
        classA:type[Element],
        classB:type[Element])->bool: 
        """
        Check if the two DataCollection are compatible 
        for the operator. 
        """
        pass


    @classmethod
    @abstractmethod
    def dot(
        cls,
        leftOperand:Element,
        rightOperand:Element)->Element:
        """
        The dot method is a classmethod that acts as a operator 
        ofdataCollections  group. It will return a new
        DataCollection with the result of the operation.
        """
        pass
    
    @classmethod
    @abstractmethod
    def signature(cls)->list[set]: 
        pass 
    
    @classmethod
    def getEleOperator(cls,targetClass:type[Element])->type[CollectionOperator] | None:    
        for subclass in cls.__subclasses__():
            if targetClass == subclass.productClass:
                return subclass
        return None 
    