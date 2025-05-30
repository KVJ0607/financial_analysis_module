from ..element import Element
from ..element import Car3Element,Car3NewsElement,NewsElement,PricingElement,NoneElement

class Space:
    _DefAULTSPACE = set([Car3Element, Car3NewsElement, NewsElement, PricingElement])
    _SPACE:set[type[Element]] = set()
    
    
    @classmethod    
    def initSpaceDefinition(cls,space): 
        if cls._SPACE:
            raise ValueError("Space definition has already been initialized. Please use a different method to modify the space.")
        for component in space:
            if not issubclass(component, Element):
                raise TypeError(f"{component} is not a subclass of Element.")
        cls._SPACE = set(space).difference(set([NoneElement]))

    
    @classmethod
    def initDefaultSpaceDefinition(cls):
        cls.initSpaceDefinition(cls._DefAULTSPACE)
        
    
    @classmethod
    def addSpaceDefinition(cls,component:type[Element]):
        """
        Add components to the group space.
        
        Args:
            *components: Components to be added to the group space.
        
        Raises:
            TypeError: If any component is not a subclass of Element.
        """
        if not cls._SPACE: 
            cls.initDefaultSpaceDefinition()
        if not issubclass(component, Element):
            raise TypeError(f"{component} is not a subclass of Element.")
        if component:
            cls._SPACE.add(component)

    @classmethod
    def getSpaceDefinition(cls)->set[type[Element]]:
        if not cls._SPACE:
            raise ValueError("Space definition has not been initialized. Please call initDefaultSpaceDefinition() or initSpaceDefinition() first.")
        return cls._SPACE
    
    @classmethod
    def emptySpaceDefinition(cls):
        """
        Empty the current space definition.
        Warning: It will affect all instances of Group. 
        """

        cls._SPACE = set(cls._DefAULTSPACE)        

    
    def __init__(self):
        if not self._SPACE:
            raise ValueError("Space definition has not been initialized. Please call initDefaultSpaceDefinition() or initSpaceDefinition() first.")
        self._cayleyTable = dict()
        for eleType in self._SPACE:
            self._cayleyTable[eleType] = NoneElement()
    
    @property
    def spaceDefinition(self)->set[type[Element]]:
        """
        Get the space definition of the group.
        
        Returns:
            set: A set containing the types of elements in the group space.
        """
        return self._SPACE      
        
    
    @property
    def cayleyTable(self)->dict[type[Element], Element]:
        return self._cayleyTable
    
    
        
    def setCayleyElement(self,ele: Element): 
        if not isinstance(ele,Element): 
            raise TypeError(f"""{ele} is of type{type(ele)}
                            but not {Element}""")
        if type(ele) not in self._SPACE:
            raise TypeError(f"""{type(ele)} is not in the space of {self._SPACE}""")
        
        self._cayleyTable[type(ele)] = ele
    
    

    def getValuedSupgroup(self)-> dict[type[Element], Element]:
        """
        Get the non-empty subgroup of the group.        
        Returns:
            dict: A dictionary containing the valued subgroup.
        """
        valuedSubgroup = dict()
        for key, value in self._cayleyTable.items():
            if value:
                valuedSubgroup[key] = value
        return valuedSubgroup    
