from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..element import Element

from abc import ABC, abstractmethod




class Operator(ABC) :     
    """ 
    Handle binary opertaion between object of DataCollection with the 
    different pointType attribute.The actual logic depends on the pointType attribute 
    from both operand.
        
    A class that provide classmethods that acts as operators between dataCollections 
    having different pointType attribute.
    """
    
    @classmethod
    @abstractmethod
    def getProductClass(cls)->type:
        pass 
        
    @classmethod
    @abstractmethod
    def getOperands(cls)->set:      
        pass         

    @classmethod
    @abstractmethod
    def dot(
        cls,
        *operand:Element
        )->Element | None:
        """
        The dot method is a classmethod that acts as a
        operator of Element. It will return a new
        Element.
        """
        pass
    

    
