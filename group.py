from __future__ import annotations
from typing import Type,Callable

from shareEntity import ShareEntity
import element_of_group

import group_operators




class Group:   

    def __init__(
        self,
        shareCode:ShareEntity|str =None,
        *args,
        ):
        
        #initGroup
        cayleyTable = {}
        for iType in element_of_group.Element.__subclasses__(): 
            cayleyTable[iType] = element_of_group.NoneElement()
        self.__cayleyTable = cayleyTable
        
                
        self.updateCayleyTableWithGroupElements(*args)                          

        
        self.shareEntity = shareCode
            
    
    
    @property
    def shareEntity(self)->ShareEntity: 
        return self.__shareEntity
    
    @shareEntity.setter
    def shareEntity(self,share): 
        self.__shareEntity = ShareEntity.createShareCode(share)
    
    
    @property
    def shareCode(self)->str: 
        return self.__shareEntity.shareCode    
    
    @shareCode.setter
    def shareCode(self,share): 
        self.__shareEntity = ShareEntity.createShareCode(share)
                                  

    @property
    def cayleyTable(self)->dict[type[element_of_group.Element],'Group']:
        return self.__cayleyTable
    
    @property
    def valuedSubgroup(self)->dict[type[element_of_group.Element],'Group']:
        valuedCayleyTable = dict()
        for iClass,iEle in self.__cayleyTable.items(): 
            if not self.nullElementClass(iClass): 
                valuedCayleyTable[iClass]=iEle
        return valuedCayleyTable
                    

    def updateCayleyTableWithGroupElements(self,*args):
        unseenClass = []
        for iArg in args: 
            if isinstance(iArg,element_of_group.Element): 
                unseenClass.append(type(iArg))
                self.__cayleyTable[type(iArg)] = iArg   
                resultClasses = iArg.getConveribleClasses()
                if resultClasses:
                    for resultClass in resultClasses: 
                        if self.nullElementClass(resultClass): 
                            self.__cayleyTable[resultClass] = iArg.convertTo(resultClass)
                            unseenClass.append(resultClass)
                    
        
        allCombination = self.__getAllCrossSignature(unseenClass)
        seenCombination = list()
        while allCombination:
            iCombination = allCombination[0]
            allCombination.remove(iCombination)             
            eleclassA = iCombination.pop()
            eleclassB = iCombination.pop()
            if iCombination not in seenCombination:
                dotProduct = self.__dot(eleclassA,eleclassB)
                seenCombination.append(set([eleclassA,eleclassB]))
                if not isinstance(dotProduct,element_of_group.NoneElement):                    
                    allCombination.extend(
                        self.__getAllCrossSignature([type(dotProduct)]))
                    self.__cayleyTable[type(dotProduct)] = dotProduct
 
    def __getAllCrossSignature(
        self,
        unseenClasses:list[type[element_of_group.Element]])->list[set[element_of_group.Element]]:
        
        allCombination = []
        currentValuedClasses = self.valuedSubgroup        
        for iC in currentValuedClasses: 
            for jC in unseenClasses: 
                if iC != jC: 
                    allCombination.append(set([iC,jC]))
        return allCombination
        
        
        
        
    def expandGroup(self,elementClass:type[element_of_group.Element]): 
        if not isinstance(elementClass,type[element_of_group.Element]):
            raise TypeError(f"{elementClass} is not of type{type[element_of_group.Element]}")        
        
        self.__cayleyTable[elementClass] = element_of_group.NoneElement()
        
        for valuedElement in self.valuedSubgroup:
            if valuedElement.convertible(elementClass):
                converted = valuedElement.convertTo(elementClass)
                self.updateCayleyTableWithGroupElements(converted)
                return True  
        
        targetOperator = (group_operators.CollectionOperator.
                          getEleOperator(elementClass))
        if targetOperator is not None: 
            for iSig in targetOperator.signature(): 
                if iSig.issubset(set(self.valuedSubgroup)): 
                    operantClassA = iSig.pop()
                    operantClassB= iSig.pop()
                    product = targetOperator.dot(
                        self.getElement(operantClassA),
                        self.getElement(operantClassB))
                    self.updateCayleyTableWithGroupElements(product)
                    return  True 
        
        return False
    
         
                    
            
    def containElementClass(
        self,
        eleClass:Type[element_of_group.Element])->bool:
        """
        Check if the collection group contain the element
        """
        if eleClass in self.__cayleyTable: 
            return True
        else: 
            return False        
        
        
    def getElement(
        self,
        eleClass:Type[element_of_group.Element])->element_of_group.Element:        
        """
        Get the element of the collection group
        """
        if eleClass in self.__cayleyTable: 
            return self.__cayleyTable[eleClass]
        else: 
            raise ValueError(f"""The element Class {eleClass.__name__}
                             doesn't belong to the group""")
    
    def nullElementClass(self,eleClass:Type[element_of_group.Element])->bool: 
        return isinstance(
            self.getElement(eleClass),
            element_of_group.NoneElement
        )
                                
    
    def __dot(
        self,
        classA:type[element_of_group.Element],
        classB:type[element_of_group.Element])->element_of_group.Element:
        
        if not (issubclass(classA,element_of_group.Element) 
            and issubclass(classB,element_of_group.Element)):
            raise TypeError(f"""{classA} and {classB} should be 
                            of a class whoses parent class is 
                            {element_of_group.Element}""")
            
        for subClass in group_operators.CollectionOperator.__subclasses__(): 
            if (subClass.match(classA,classB)
                and not self.containElementClass(
                    subClass.productClass)
                ):
                targetEle = subClass.dot(
                    self.getElement(classA),
                    self.getElement(classB))     
        
                return targetEle                
        return element_of_group.NoneElement
    
            
    def joinGroupTable(self,groupB:Group):    
        if not isinstance(groupB,Group):
            raise TypeError(f"""{groupB} should be of 
                            class {Group} but 
                            not {type(groupB)}""")
        
        elementsToBeUpdates = []
        for key,value in groupB.cayleyTable.items(): 
            if (key in self.cayleyTable 
                and (not isinstance(value,element_of_group.NoneElement))
                and isinstance(self.getElement(key),element_of_group.NoneElement)): 
                elementsToBeUpdates.append(value)                
        self.updateCayleyTableWithGroupElements(*elementsToBeUpdates)    


    @classmethod 
    def normalizeAllGroups(
        cls,
        *args
    ): 
        groups = list(args)
        if len(groups) <2: 
            raise Exception()
        if not isinstance(groups[0],Group): 
            raise TypeError("args have to be objects of type Group")
        firstGroup = groups[0]
        
        for iClass in firstGroup.valuedSubgroup:
            hashInFirstGroup = set(
                firstGroup.getElement(iClass).
                inList.keys()
            )
                        
            hashsInOtherGroups =[]
            for JGroup in groups[1:]:
                JGroup:Group
                hashsInOtherGroups.append(
                    JGroup.getElement(iClass).inList.keys()
                    )
                
            hashsIntersection = (
                hashInFirstGroup.intersection(hashsInOtherGroups)                    
            )
            
            for JGroup in groups: 
                hashInJGroup = set(
                    JGroup.getElement(iClass).inList.keys()
                )
                iBadHash = hashInJGroup.difference(hashsIntersection)
                iEleInJGroup = JGroup.getElement(iClass).inList
                
                
        
                
    

    @classmethod
    def operateElementwiseInAClassSpace(
        self,
        groupA:Group,
        groupB:Group,
        spaceOfClass:type[element_of_group.Element],
        pointwiseOperation:Callable)->element_of_group.Element:
        
        if not groupA.containElementClass(spaceOfClass): 
            groupA.expandGroup(spaceOfClass)
            
        if not groupB.containElementClass(spaceOfClass): 
            groupB.expandGroup(spaceOfClass) 
            
        
        
        spaceElementA = groupA.getElement(spaceOfClass)
        spaceElementB = groupB.getElement(spaceOfClass)
        if isinstance(spaceElementA,element_of_group.NoneElement): 
            raise ValueError(f"""{groupA} don't have point class 
                            {spaceOfClass} data""")
        elif isinstance(spaceElementB,element_of_group.NoneElement): 
            raise ValueError(f"""{groupA} don't have point class {
                spaceOfClass} data""")
        
        products= []            
        for aHash in spaceElementA.inList: 
            if aHash in spaceElementB.inList: 
                products.append(pointwiseOperation(
                    spaceElementA.inList[aHash],
                    spaceElementB.inList[aHash]
                ))
        return type(spaceElementA)(products)
                    
                
                
                
            
        
