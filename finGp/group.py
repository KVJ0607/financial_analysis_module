from __future__ import annotations
from typing import Type, Callable

from .shareEntity import ShareEntity
from . import element_of_group
from .import group_operators


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
        for iType in element_of_group.Element.__subclasses__():
            if iType != element_of_group.NoneElement: 
                cayleyTable[iType] = element_of_group.NoneElement()
        self.__cayleyTable = cayleyTable

        # Update Cayley table with provided elements
        self.updateCayleyTableWithGroupElements(*args)

        # Set the share entity
        self.shareEntity = shareCode

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

    @property
    def cayleyTable(self) -> dict[type[element_of_group.Element], element_of_group.Element]:
        """
        Get the Cayley table of the group.

        Returns:
            dict: The Cayley table mapping element types to group elements.
        """
        return self.__cayleyTable
    

    @property
    def valuedSubgroup(self) -> dict[type[element_of_group.Element], 'Group']:
        """
        Get the valued subgroup of the group.

        Returns:
            dict: A dictionary of element types and their corresponding group elements
                  that are not NoneElement.
        """
        valuedCayleyTable = dict()
        for iClass, iEle in self.__cayleyTable.items():
            if not self.nullElementClass(iClass):
                valuedCayleyTable[iClass] = iEle
        return valuedCayleyTable
    


    def updateCayleyTableWithGroupElements(self, *args):
        """
        Update the Cayley table with the provided elements.

        Args:
            *args: Elements to add to the Cayley table.
        """
        unseenClasses = []
        for iArg in args:
            if isinstance(iArg, element_of_group.Element):
                unseenClasses.append(type(iArg))
                self.__cayleyTable[type(iArg)] = iArg
                resultClasses = iArg.getConveribleClasses()
                if resultClasses:
                    for resultClass in resultClasses:
                        if not self.nullElementClass(resultClass):
                            self.__cayleyTable[resultClass] = iArg.convertTo(resultClass)
                            unseenClasses.append(resultClass)

        allCombination = self.__getAllCrossSignature(unseenClasses)
        seenCombination = list()

        while allCombination:
            iCombination = allCombination.pop()
            if iCombination not in seenCombination:
                eleclassA = iCombination.pop()
                eleclassB = iCombination.pop()
                dotProduct = self.__dot(eleclassA, eleclassB)
                seenCombination.append(set([eleclassA, eleclassB]))
                if not isinstance(dotProduct, element_of_group.NoneElement):
                    allCombination.extend(
                        self.__getAllCrossSignature([type(dotProduct)]))
                    self.__cayleyTable[type(dotProduct)] = dotProduct

    def __getAllCrossSignature(
        self,
        unseenClasses: list[type[element_of_group.Element]]
    ) -> list[set[element_of_group.Element]]:

        allCombination = []
        for iC in self.valuedSubgroup:
            for jC in unseenClasses:
                if (iC != jC
                        and set([jC, iC]) not in allCombination):
                    allCombination.append(set([iC, jC]))
        return allCombination


    def __dot(
        self,
        classA: type[element_of_group.Element],
        classB: type[element_of_group.Element]
    ) -> element_of_group.Element:
        if not (issubclass(classA, element_of_group.Element)
                and issubclass(classB, element_of_group.Element)):
            raise TypeError(f"""{classA} and {classB} should be 
                            of a class whose parent class is 
                            {element_of_group.Element}""")

        for subClass in group_operators.CollectionOperator.__subclasses__():
            if (subClass.match(classA, classB)
                    and not self.containElementClass(
                        subClass.productClass)
                    ):
                targetEle = subClass.dot(
                    self.getElement(classA),
                    self.getElement(classB))

                return targetEle
        return element_of_group.NoneElement()


    def expandGroup(self, elementClass: type[element_of_group.Element]):
        """
        Expand the group by adding a new element class.

        Args:
            elementClass (type): The element class to add.

        Raises:
            TypeError: If the provided class is not a subclass of Element.

        Returns:
            bool: True if the group was successfully expanded, False otherwise.
        """
        if not isinstance(elementClass, type[element_of_group.Element]):
            raise TypeError(f"{elementClass} is not of type{type[element_of_group.Element]}")

        self.__cayleyTable[elementClass] = element_of_group.NoneElement()

        for valuedElement in self.valuedSubgroup:
            if valuedElement.convertible(elementClass):
                converted = valuedElement.convertTo(elementClass)
                self.updateCayleyTableWithGroupElements(converted)
                return True

        targetOperator = (group_operators.CollectionOperator.
                          getOperator(elementClass))
        if targetOperator is not None:
            for iSig in targetOperator.signatures():
                if iSig.issubset(set(self.valuedSubgroup)):
                    operantClassA = iSig.pop()
                    operantClassB = iSig.pop()
                    product = targetOperator.dot(
                        self.getElement(operantClassA),
                        self.getElement(operantClassB))
                    self.updateCayleyTableWithGroupElements(product)
                    return True

        return False

    def containElementClass(
        self,
        eleClass: Type[element_of_group.Element]
    ) -> bool:
        """
        Check if the group contains an element of the specified class.

        Args:
            eleClass (Type): The element class to check.

        Returns:
            bool: True if the group contains the element, False otherwise.
        """
        return eleClass in self.__cayleyTable

    def getElement(
        self,
        eleClass: Type[element_of_group.Element]
    ) -> element_of_group.Element:
        """
        Get the element of the specified class from the group.

        Args:
            eleClass (Type): The element class to retrieve.

        Returns:
            Element: The element of the specified class.

        Raises:
            ValueError: If the element class is not found in the group.
        """
        if eleClass in self.__cayleyTable:
            return self.__cayleyTable[eleClass]
        else:
            raise ValueError(f"""The element Class {eleClass}
                             doesn't belong to the group""")
            
    def getDataPoins(
        self,
        eleClass: Type[element_of_group.Element]
    ) -> list[element_of_group.DataPoint]: 
        ele = self.getElement(eleClass)
        dataPoints = []
        for iPoint in ele.inDict.values():
            dataPoints.append(dataPoints)
        return dataPoints

    def nullElementClass(self, eleClass: Type[element_of_group.Element]) -> bool:
        """
        Check if the specified element class is a NoneElement.

        Args:
            eleClass (Type): The element class to check.

        Returns:
            bool: True if the element class is a NoneElement, False otherwise.
        """
        return isinstance(
            self.getElement(eleClass),
            element_of_group.NoneElement
        )


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
        for key, value in groupB.cayleyTable.items():
            if (key in self.cayleyTable
                    and (not isinstance(value, element_of_group.NoneElement))
                    and isinstance(self.getElement(key), element_of_group.NoneElement)):
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
                jGroup.cayleyTable[iClass] = goodElement

    @classmethod
    def operateElementwiseInAClassSpace(
        cls,
        groupA: Group,
        groupB: Group,
        spaceOfClass: type[element_of_group.Element],
        pointwiseOperation: Callable
    ) -> element_of_group.Element:
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
        if not groupA.containElementClass(spaceOfClass):
            groupA.expandGroup(spaceOfClass)

        if not groupB.containElementClass(spaceOfClass):
            groupB.expandGroup(spaceOfClass)

        spaceElementA = groupA.getElement(spaceOfClass)
        spaceElementB = groupB.getElement(spaceOfClass)
        if isinstance(spaceElementA, element_of_group.NoneElement):
            raise ValueError(f"""{groupA} doesn't have point class 
                            {spaceOfClass} data""")
        elif isinstance(spaceElementB, element_of_group.NoneElement):
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






