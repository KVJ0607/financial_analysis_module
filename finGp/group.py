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
        shareCode: ShareEntity | str = None,
        *args,
    ):
        """
        Initialize a Group instance.

        Args:
            shareCode (ShareEntity | str, optional): The share code or entity associated with the group.
            *args: Elements to initialize the group with.
        """
        # Initialize Cayley table with NoneElement for all subclasses of Element
        cayleyTable = {}
        for iType in element.Element.__subclasses__():
            if iType != element.NoneElement: 
                cayleyTable[iType] = element.NoneElement()
        self.__cayleyTable = cayleyTable

        # Update Cayley table with provided elements
        self.updateCayleyTableWithGroupElements(*args)

        # Set the share entity
        self.shareEntity = shareCode

    def __str__(self):
        selfStr =  f'share:{self.shareCode}'
        for subclass in element.Element.__subclasses__(): 
            if self.containElementData(subclass):
                selfStr += f"""\n{subclass} have {len(self.getElement(subclass).inDict)} Data"""
            else: 
                selfStr+=f"""\n{subclass} is empty"""
        return selfStr
        
    @property
    def shareEntity(self) -> ShareEntity:
        return self.__shareEntity

    @shareEntity.setter
    def shareEntity(self, share):
        self.__shareEntity = ShareEntity.createShareCode(share)

    @property
    def shareCode(self) -> str:
        return self.__shareEntity.shareCode

    @shareCode.setter
    def shareCode(self, share):
        self.__shareEntity = ShareEntity.createShareCode(share)

    # @property
    # def cayleyTable(self) -> dict[type[element.Element], element.Element]:
    #     """
    #     Get the Cayley table of the group.

    #     Returns:
    #         dict: The Cayley table mapping element types to group elements.
    #     """
    #     return self.__cayleyTable
    

    @property
    def valuedSubgroup(self) -> dict[type[element.Element], 'Group']:
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
        if not isinstance(ele,element.Element): 
            raise TypeError(f"""{ele} is of type{type(ele)}
                            but not {element.Element}""")
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
        eleClass: Type[element.Element]
    ) -> element.Element:
        """
        Retrieve an element of the specified class from the Cayley table.

        Args:
            eleClass (Type[element.Element]): The class of the element to retrieve.

        Returns:
            element.Element: The retrieved element.

        Raises:
            TypeError: If the provided class is not a subclass of element.Element.
            ValueError: If the element class cannot be resolved for the group.
        """
        if not issubclass(eleClass, element.Element):
            raise TypeError(f"{eleClass} is not a subclass of {element.Element}")

        # Check if the element exists in the valued subgroup
        if eleClass in self.valuedSubgroup:
            return self.__cayleyTable[eleClass]

        # Attempt to find convertible classes
        convertibleClasses = element.Element.getClassThatCanConvertedTo(eleClass)
        if convertibleClasses:
            for conClass in convertibleClasses:
                if self.containElementData(conClass):
                    self.__cayleyTable:dict[Type[element.Element],element.Element]
                    resultElement = self.__cayleyTable.get(conClass).convertTo(eleClass)
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
        print(f"Warning: Unable to resolve element of class {eleClass} for group {self}")
        return element.NoneElement()
    


                
    def getDataPoins(
        self,
        eleClass: Type[element.Element]
    ) -> list[element.DataPoint]:      
        
        ele = self.getElement(eleClass)
        dataPoints = []
        for iPoint in ele.inDict.values():
            dataPoints.append(iPoint)
        return dataPoints


    def inCayleyTable(self, eleClass: Type[element.Element]) -> bool:
        """
        Check if the given element class is registered in the Cayley table.

        Args:
            eleClass (Type[element.Element]): The element class to check.

        Returns:
            bool: True if the element class is in the Cayley table, False otherwise.
        """
        return eleClass in self.__cayleyTable
            
            
    def containElementData(self, eleClass: Type[element.Element]) -> bool:
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
        """
        Normalize all groups by finding common elements across multiple groups and updating their Cayley tables.
        This method takes multiple `Group` objects, identifies common valued subgroups, and computes the intersection
        of hash sets for each common subgroup. It then updates the Cayley table of each group with the normalized elements.
        Args:
            cls: The class reference (used for class methods).
            *args: A variable number of `Group` objects to be normalized.
        Raises:
            Exception: If fewer than two groups are provided.
        Notes:
            - The method assumes that each `Group` object has the following attributes and methods:
                - `valuedSubgroup`: A dictionary containing subgroup values.
                - `getElement(iClass)`: A method that retrieves an element of the group for a given class.
                - `cayleyTable`: A dictionary representing the group's Cayley table.
                - `hashSet`: A set of hash values associated with a group element.
                - `inDict`: A dictionary mapping hash values to points.
            - The `iClass` is expected to be callable to create a new element with a list of points.
        """        
        
        groups: list[Group] = list(args)

        if len(groups) < 2:
            raise Exception()

        firstGroup = groups[0]
                    
        
        commonValuedGroup = set(
            firstGroup.valuedSubgroup.keys()
        )
        
        
        for iGroup in groups[1:]:
            commonValuedGroup.intersection_update(iGroup.valuedSubgroup.keys())
        

        for iClass in commonValuedGroup:
            hashsIntersection = groups[0].getElement(iClass).hashSet

            for jGroup in groups[1:]:
                jGroup: Group
                hashsIntersection.intersection_update(
                    jGroup.getElement(iClass).hashSet
                )
                

            for jGroup in groups:
                iEleInJGroup = jGroup.getElement(iClass).inDict
                goodPoints = [
                    v for k, v in iEleInJGroup.items() if k in hashsIntersection
                ]
                goodElement = iClass(goodPoints)
                jGroup.__cayleyTable[iClass] = goodElement

    @classmethod
    def operateElementwiseInAClassSpace(
        cls,
        groupA: Group,
        groupB: Group,
        spaceOfClass: type[element.Element],
        pointwiseOperation: Callable
    ) -> element.Element:
        """
        Perform an element-wise operation in a specific class space.

        Args:
            groupA (Group): The first group.
            groupB (Group): The second group.
            spaceOfClass (type): The class space to operate in.
            pointwiseOperation (Callable): The operation to perform.

        Returns:
            Element: The resulting element from the operation.

        Raises:
            ValueError: If the required element class is not found in either group.
        """
        
        if not issubclass(spaceOfClass,element.Element):
            print(f"""Waring: {spaceOfClass} 
                  is not a subclass of {element.Element}""")
            return element.NoneElement
        
        if not groupA.containElementData(spaceOfClass):
            groupA.__cayleyTable[spaceOfClass]= element.NoneElement()

        if not groupB.containElementData(spaceOfClass):
            groupB.__cayleyTable[spaceOfClass] = element.NoneElement()

        spaceElementA = groupA.getElement(spaceOfClass)
        spaceElementB = groupB.getElement(spaceOfClass)
        if isinstance(spaceElementA, element.NoneElement):
            raise ValueError(f"""{groupA} doesn't have point class 
                            {spaceOfClass} data""")
        elif isinstance(spaceElementB, element.NoneElement):
            raise ValueError(f"""{groupB} doesn't have point class 
                            {spaceOfClass} data""")

        products = []
        for aHash in spaceElementA.inDict:
            if aHash in spaceElementB.inDict:
                products.append(pointwiseOperation(
                    spaceElementA.inDict[aHash],
                    spaceElementB.inDict[aHash]
                ))
        return type(spaceElementA)(products)






