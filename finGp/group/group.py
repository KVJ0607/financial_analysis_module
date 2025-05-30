from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:    
    from ..element import Element

from .._shareEntity import ShareEntity
from .. import operation

from .setops import SetOps
from .space import Space

class Group:
    """
    A class representing a collection of elements grouped together. This class
    provides methods to manage, manipulate, and operate on elements within the group.

    The group maintains a Cayley table to store elements and their relationships.
    It supports operations such as expanding the group, joining groups, and normalizing
    multiple groups.
    """
    _operationTableCls = operation.OperationTable
    
    def __init__(
        self,
        share: ShareEntity | str = None,
        *args: Element,
    ):
        """
        Initialize a Group instance.

        Args:
            share (ShareEntity | str, optional): The share code or entity associated with the group.
            *args: Elements to initialize the group with.
        """
        self._space = Space()

        # Update Cayley table with provided elements
        for iArg in args:
            self._space.setCayleyElement(iArg)

        # Set the share entity
        self._shareEntity = ShareEntity.createShareEntity(share)

        


    @property
    def shareCode(self) -> str:
        return self._shareEntity.shareCode



    def update(self): 
        for iClass in self._space.spaceDefinition:
            self._getElementByType(iClass)    
    


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
        for key, value in groupB._space.cayleyTable.items():
            if value and key not in self._space.getValuedSupgroup():
                elementsToBeUpdates.append(value)
        for ele in elementsToBeUpdates:
            self._space.setCayleyElement(ele)

    

            
    def acceptOutVisitor(self, destDir: str):
        import os
        import csv
        destDir = os.path.splitext(destDir)[0]
        os.makedirs(destDir, exist_ok=True)
        for iClass, iEle in self._space.getValuedSupgroup().items():
            destVar = os.path.join(destDir, iClass.__name__ + ".csv")
            with open(destVar, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = None
                for iPoint in iEle:
                    iDict = iPoint.toJson()
                    if writer is None:
                        writer = csv.DictWriter(csvfile, fieldnames=iDict.keys())
                        writer.writeheader()
                    writer.writerow(iDict)
                
                
                

    def _getElementByType(self, elementType: type[Element],depth:int = 0) -> Element | None:
        MAX_DEPTH = 10
        if depth > MAX_DEPTH:
            raise RecursionError(f"Maximum recursion depth of {MAX_DEPTH} exceeded while trying to retrieve element of type {elementType}.")
        """
        Get an element of a specific type from the group.

        Args:
            elementType (type[Element]): The type of the element to retrieve.

        Returns:
            Element: An instance of the specified element type, or None if not found.
        """
        
        if not isinstance(elementType, type) or not elementType in self._space.spaceDefinition:
            raise TypeError(f"{elementType} is not a valid element type in the group space definition.")
        
        # Retrive element from the Cayley table
        if elementType in self._space.getValuedSupgroup():            
            return self._space.cayleyTable[elementType]
        
        # If not found, resort to operation table
        for productClass, tableMember in self._operationTableCls.getOperationTable().items():
            if (productClass == elementType):
                if tableMember.getOperands().issubset(self._space.getValuedSupgroup()):
                    targetElement = tableMember.getOperator().dot(
                        *[self._space.cayleyTable[iClass] for iClass in tableMember.getOperands()]
                    )
                    self._space.setCayleyElement(targetElement)                    
                    return targetElement
                else: 
                    allOperandsFound = True
                    for Operand in tableMember.getOperands().difference(self._space.getValuedSupgroup()):
                        thisOperand = self._getElementByType(Operand,depth+1)
                        if not thisOperand:
                            allOperandsFound = False 
                            break
                    if allOperandsFound:
                        targetElement = tableMember.getOperator().dot(
                            *[self._space.cayleyTable[iClass] for iClass in tableMember.getOperands()]
                        )
                        self._space.setCayleyElement(targetElement)                    
                        return targetElement
        # If no element of the specified type is found, return None                    
        return None
    
    @classmethod
    def getSpaceDefinitionCls(cls) -> type[Space]:
        return Space
    
    @classmethod
    def normalizeAllGroups(
        cls,
        *args:Group,      
    ):   
                
        groups: list[Group] = list(args)
        if len(groups) < 2:
            raise ValueError("At least two groups are required for normalization.")

        commonValuedGroups = set(groups[0]._space.getValuedSupgroup().keys())
        for iGroup in groups[1:]:
            commonValuedGroups = commonValuedGroups.intersection(iGroup._space.getValuedSupgroup().keys())         
            
        for iClass in commonValuedGroups:            
            goodElements = SetOps.intersectMany(
                *[x._getElementByType(iClass) for x in groups if x._space.cayleyTable[iClass]]
                )            
            
            for j,jGroup in enumerate(groups):
                jGroup._space.setCayleyElement(goodElements[j])

    





