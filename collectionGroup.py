from __future__ import annotations
from typing import Type,Callable

from shareEntity import ShareEntity
import point

import group_operators




class CollectionGroup:   

    def __init__(
        self,
        shareCode:ShareEntity|str =None,
        *args,
        ):
        
        #initGroup
        cayleyTable = {}
        for iType in point.DataPoint.__subclasses__(): 
            cayleyTable[iType] = point.NoneDataPoint.getGroupElement()
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
    def cayleyTable(self)->dict[type[point.DataPoint],'CollectionGroup']:
        return self.__cayleyTable
    
    @property
    def valuedSubgroup(self)->dict[type[point.DataPoint],'CollectionGroup']:
        valuedCayleyTable = dict()
        for iClass,iEle in self.__cayleyTable.items(): 
            if not self.nullElementClass(iClass): 
                valuedCayleyTable[iClass]=iEle
        return valuedCayleyTable
                    

    def updateCayleyTableWithGroupElements(self,*args):
        unseenClass = []
        for iArg in args: 
            if isinstance(iArg,point.GroupElement): 
                unseenClass.append(iArg.eleClass)
                self.__cayleyTable[iArg.eleClass] = iArg   
                resultClasses = iArg.getConvertResultClasses()
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
                if not isinstance(dotProduct,point.NoneElement):                    
                    allCombination.extend(
                        self.__getAllCrossSignature([dotProduct.eleClass]))
                    self.__cayleyTable[dotProduct.eleClass] = dotProduct
 
    def __getAllCrossSignature(
        self,
        unseenClasses:list[type[point.DataPoint]])->list[set[point.GroupElement]]:
        
        allCombination = []
        currentValuedClasses = self.valuedSubgroup        
        for iC in currentValuedClasses: 
            for jC in unseenClasses: 
                if iC != jC: 
                    allCombination.append(set([iC,jC]))
        return allCombination
        
        
        
        
    def expandGroup(self,elementClass:type[point.DataPoint]): 
        if not isinstance(elementClass,type[point.DataPoint]):
            raise TypeError(f"{elementClass} is not of type{type[point.DataPoint]}")        
        
        self.__cayleyTable[elementClass] = point.NoneDataPoint.getGroupElement()
        
        for valuedClass in self.valuedSubgroup:
            valuedGroup = valuedClass.getTypeGroupElement()
            if valuedGroup.convertible(elementClass):
                converted = valuedGroup.convertTo(elementClass)
                self.updateCayleyTableWithGroupElements(converted)
                return True  
        
        targetOperator = group_operators.CollectionOperator.getEleOperator(elementClass)
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
    
         
                    
            
    def containElementClass(self,eleClass:Type[point.DataPoint])->bool:
        """
        Check if the collection group contain the element
        """
        if eleClass in self.__cayleyTable: 
            return True
        else: 
            return False        
        
        
    def getElement(self,eleClass:Type[point.DataPoint])->point.GroupElement:        
        """
        Get the element of the collection group
        """
        if eleClass in self.__cayleyTable: 
            return self.__cayleyTable[eleClass]
        else: 
            raise ValueError(f"The element Class {eleClass.__name__} doesn't belong to the group")
    
    def nullElementClass(self,eleClass:Type[point.DataPoint])->bool: 
        return isinstance(
            self.getElement(eleClass),
            point.NoneElement
        )
                                
    
    def __dot(self,classA:type[point.DataPoint],classB:type[point.DataPoint])->point.GroupElement:
        if (classA not in point.DataPoint.__subclasses__()
            or classB not in point.DataPoint.__subclasses__()):
            raise TypeError(f"""{classA} and {classB} should be 
                            of a class whoses parent class is 
                            {point.DataPoint}""")
            
        for subClass in group_operators.CollectionOperator.__subclasses__(): 
            if (subClass.match(classA,classB)
                and not self.containElementClass(
                    subClass.pointClassToBeReturned)
                ):
                targetEle = subClass.dot(
                    self.getElement(classA),
                    self.getElement(classB))     
        
                return targetEle                
        return point.NoneDataPoint.getGroupElement()
    
    # @staticmethod                                                 
    # def getEleWithDot()
                 
            
    def joinGroupTable(self,groupB:CollectionGroup):    
        if not isinstance(groupB,CollectionGroup):
            raise TypeError(f"""{groupB} should be of 
                            class {CollectionGroup} but 
                            not {type(groupB)}""")
        
        elementsToBeUpdates = []
        for key,value in groupB.cayleyTable.items(): 
            if (key in self.cayleyTable 
                and (not isinstance(value,point.NoneElement))
                and isinstance(self.getElement(key),point.NoneElement)): 
                elementsToBeUpdates.append(value)                
        self.updateCayleyTableWithGroupElements(*elementsToBeUpdates)    


    @classmethod
    def operateOfelementInClassSpace(
        self,
        groupA:CollectionGroup,
        groupB:CollectionGroup,
        spaceOfClass:type[point.DataPoint],
        pointwiseOperation:Callable)->point.GroupElement:
        
        if not groupA.containElementClass(spaceOfClass): 
            groupA.expandGroup(spaceOfClass)
            
        if not groupB.containElementClass(spaceOfClass): 
            groupB.expandGroup(spaceOfClass) 
            
        
        
        spaceElementA = groupA.getElement(spaceOfClass)
        spaceElementB = groupB.getElement(spaceOfClass)
        if isinstance(spaceElementA,point.NoneElement): 
            raise ValueError(f"""{groupA} don't have point class 
                            {spaceOfClass} data""")
        elif isinstance(spaceElementB,point.NoneElement): 
            raise ValueError(f"""{groupA} don't have point class {
                spaceOfClass} data""")
        
        products= []            
        for aHash in spaceElementA.element: 
            if aHash in spaceElementB.element: 
                products.append(pointwiseOperation(
                    spaceElementA.element[aHash],
                    spaceElementB.element[aHash]
                ))
        return spaceElementA.eleClass.getGroupElement(products)
                    
                
                
                
            
        
