from __future__ import annotations
from typing import Type, Callable

from .shareEntity import ShareEntity
from . import element
from .import operator


class Group:
    """
    A class representing a collection of elements grouped together. This class
    provides methods to manage, manipulate, and operate on elements within the group.

    The group maintains a Cayley table to store elements and their relationships.
    It supports operations such as expanding the group, joining groups, and normalizing
    multiple groups.
    """

    def __init__(
        self,
        share: ShareEntity | str = None,
        *args,
    ):
        """
        Initialize a Group instance.

        Args:
            share (ShareEntity | str, optional): The share code or entity associated with the group.
            *args: Elements to initialize the group with.
        """
        # Initialize Cayley table with NoneElement for all subclasses of Element
        cayleyTable = {}
        for iType in element.ElementBase.__subclasses__():
            if iType != element.NoneElement: 
                cayleyTable[iType] = element.NoneElement()
        self.__cayleyTable = cayleyTable

        # Update Cayley table with provided elements
        self.updateCayleyTableWithGroupElements(*args)

        # Set the share entity
        self.shareEntity = share

    def __str__(self):
        selfStr =  f'share:{self.shareCode}'
        for subclass in element.ElementBase.__subclasses__(): 
            if self.containElementData(subclass):
                selfStr += f"""\n{subclass} have {len(self.getElement(subclass).dataPoints)} Data"""
            else: 
                selfStr+=f"""\n{subclass} is empty"""
        return selfStr
        
    @property
    def shareEntity(self) -> ShareEntity:
        return self.__shareEntity

    @shareEntity.setter
    def shareEntity(self, share):
        self.__shareEntity = ShareEntity.createShareEntity(share)

    @property
    def shareCode(self) -> str:
        return self.__shareEntity.shareCode


    

    @property
    def valuedSubgroup(self) -> dict[type[element.ElementBase], 'Group']:
        """
        Get the valued subgroup of the group.

        Returns:
            dict: A dictionary of element types and their corresponding group elements
                  that are not NoneElement.
        """
        valuedCayleyTable = dict()
        for iClass, iEle in self.__cayleyTable.items():
            if self.containElementData(iClass):
                valuedCayleyTable[iClass] = iEle
        return valuedCayleyTable
    
    def setCayleyElement(self,ele): 
        if not isinstance(ele,element.ElementBase): 
            raise TypeError(f"""{ele} is of type{type(ele)}
                            but not {element.ElementBase}""")
        if isinstance(ele,element.NoneElement): 
            print(f"""Warning class {type(ele)} to None
                  in cayleyElement of {self.shareCode}""")
            return None
        
        self.__cayleyTable[type(ele)] = ele

    def updateCayleyTableWithGroupElements(self, *args):
        """
        Update the Cayley table with the provided elements.

        Args:
            *args: Elements to add to the Cayley table.
        """
        
        for iArg in args:
            self.setCayleyElement(iArg)



    def getElement(
        self,
        eleTemplate: element.ElementBase|type[element.ElementBase]
    ) -> element.ElementBase:
        """
        Retrieve an element of the specified class from the Cayley table.

        Args:
            eleTemplate (element.Element|type[element.Element]): The element to retrieve.

        Returns:
            element.Element: The retrieved element.

        Raises:
            TypeError: If the provided class is not a subclass of element.Element.
            ValueError: If the element class cannot be resolved for the group.
        """
        
        

        if isinstance(eleTemplate,type):
            if issubclass(eleTemplate,element.ElementBase):
                eleClass = eleTemplate
        elif isinstance(eleTemplate,element.ElementBase): 
            eleClass = type(eleTemplate)
        else: 
            raise TypeError("")    
        
            
        # Check if the element exists in the valued subgroup
        if eleClass in self.valuedSubgroup:
            return self.__cayleyTable[eleClass]

        # Attempt to find convertible classes
        convertibleClasses = element.ConversionMixin.getClassThatCanConvertedTo(eleClass)
        if convertibleClasses:
            for conClass in convertibleClasses:
                if self.containElementData(conClass):
                    self.__cayleyTable:dict[Type[element.ElementBase],element.ElementBase]
                    resultElement = self.__cayleyTable.get(conClass).convertTo(eleTemplate)
                    self.setCayleyElement(resultElement)
                    return resultElement

        # Attempt to resolve using an operator
        targetOperator = operator.Operator.getOperatorforTargetClass(eleClass)
        if targetOperator:
            for signature in targetOperator.getSignatures():
                if all(sig in self.valuedSubgroup for sig in signature):
                    operands = [self.__cayleyTable[sig] for sig in signature]
                    resultElement = targetOperator.dot(*operands)
                    self.setCayleyElement(resultElement)
                    print(f"Type: {type(resultElement)}")
                    return resultElement

        # If no resolution is possible, return NoneElement
        print(f"Warning: Unable to resolve element of class {eleClass} for group {self.shareCode}")
        return element.NoneElement()
    


                


    def inCayleyTable(self, eleClass: Type[element.ElementBase]) -> bool:
        """
        Check if the given element class is registered in the Cayley table.

        Args:
            eleClass (Type[element.Element]): The element class to check.

        Returns:
            bool: True if the element class is in the Cayley table, False otherwise.
        """
        return eleClass in self.__cayleyTable
            
            
    def containElementData(self, eleClass: Type[element.ElementBase]) -> bool:
        """
        Check if the Cayley table has an element of the given class.

        Args:
            eleClass (Type[element.Element]): The element class to check.

        Returns:
            bool: True if the element exists, False otherwise.
        """
        if self.inCayleyTable(eleClass):
            ele = self.__cayleyTable[eleClass]
            return not isinstance(ele,element.NoneElement)

        return False


    def joinGroupTable(self, groupB: Group):
        """
        Join the Cayley table of another group with this group.

        Args:
            groupB (Group): The group to join with.

        Raises:
            TypeError: If the provided group is not of type Group.
        """
        if not isinstance(groupB, Group):
            raise TypeError(f"""{groupB} should be of 
                            class {Group} but 
                            not {type(groupB)}""")

        elementsToBeUpdates = []
        for key, value in groupB.__cayleyTable.items():
            if (key in self.__cayleyTable
                    and (not isinstance(value, element.NoneElement))
                    and isinstance(self.getElement(key), element.NoneElement)):
                elementsToBeUpdates.append(value)
        self.updateCayleyTableWithGroupElements(*elementsToBeUpdates)
        
        
    @classmethod
    def normalizeAllGroups(
        cls,
        *args
    ):   
        
        groups: list[Group] = list(args)

        if len(groups) < 2:
            raise Exception()

        firstGroup = groups[0]
                    
        
        commonElement = set(
            firstGroup.valuedSubgroup.keys()
        )
        
        
        for iGroup in groups[1:]:
            commonElement.intersection_update(iGroup.valuedSubgroup.keys())
        
        # Filter commonElement to only include classes that implement SetOpsMixin
        commonElement = {cls for cls in commonElement if issubclass(cls, element.SetOpsMixin)}
        
        for iClass in commonElement:
            goodElements = iClass.intersectMany(*[x.getElement(iClass) for x in groups])
            
            
            for i,jGroup in enumerate(groups):
                jGroup.__cayleyTable[iClass] = goodElements[i]







