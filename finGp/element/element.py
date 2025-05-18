from __future__ import annotations
from abc import ABC,abstractmethod


from ..date_utils.dateRepresentation import DateRepresentation

class DataPoint(ABC):        

    def __str__(self): 
        pass 
    
    @abstractmethod
    def __hash__(self):
        """Note that only int with preceding digits 20-99 is avaiable
        int with preceding digits 10-19 is reserved
        """
        pass

    @property
    @abstractmethod
    def date(self)->DateRepresentation:
        pass
    
    @property
    @abstractmethod
    def correspondingGroupElement(self)->type[Element]:                        
        pass        

                
    @abstractmethod
    def valid(self)->bool:  
        pass 
    

    @classmethod
    @abstractmethod
    def getGroupElement(cls,points:list['DataPoint'])->Element: 
        pass 
    
    @classmethod
    @abstractmethod
    def getTypeGroupElement(cls)->type[Element]:
        pass 





class Element(ABC): 

    def __len__(self): 
        """
        Return the number of DataPoint
        """    
        return len(self.items)
    
    @property
    @abstractmethod
    def pointType(self)->type[DataPoint]: 
        pass                             



    @property
    @abstractmethod
    def items(self):
        """
        Returns an iterable view of (key, DataPoint) pairs contained in this Element,
        allowing iteration over all DataPoints without exposing the internal storage structure.
        """
                    
            
    @abstractmethod
    def acceptVistor(
        self,
        v):
        pass

    @abstractmethod
    def acceptOutVistor(
        self,
        v,
        dest:str): 
        """call the corrsponding method in v
        """        
        pass 
    
    @abstractmethod
    def convertTo(self,targetTemplate:Element | type[Element])->Element:
        pass 
    
    
    @classmethod
    @abstractmethod
    def convertible(
        cls,
        targetClass:type[Element]
        )->bool:
        pass 
                       

    
    @classmethod
    @abstractmethod
    def getConveribleClasses(cls)->list[type[Element]]:
        """Return a list of type[Element] that can be 
        converted by this Element class
        """        
        pass 

    
        
        
            
    @classmethod
    def getClassThatCanConvertedTo(
        cls,
        targetClass) -> list[type[Element]]:
        classes = []
        for subclass in cls.__subclasses__(): 
            if subclass.convertible(targetClass):
                classes.append(subclass)
        return classes        


    @abstractmethod
    def intersect(self, other: 'Element') -> 'Element':
        """
        Return a new Element containing only the DataPoints that are present in both
        this Element and the other Element, as determined by their identity or hash.

        Args:
            other (Element): Another Element to intersect with.

        Returns:
            Element: A new Element instance with the intersection of DataPoints.
        """
   
    @abstractmethod
    @classmethod
    def intersectMany(cls, *elements: 'Element') -> list['Element']:
        """
        Return a list of Elements, where each element is the intersection of that element
        with all the others in the provided arguments.

        Args:
            *elements (Element): Two or more Element instances to intersect.

        Returns:
            list[Element]: A list of Element instances, each intersected with all others.

        Raises:
            ValueError: If fewer than two elements are provided.
        """
