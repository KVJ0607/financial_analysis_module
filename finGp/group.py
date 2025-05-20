from __future__ import annotations




from ._shareEntity import ShareEntity
from .import _operator

from .element import Element,SetOps,Conversion,Registry,elements
from .element._helpers.setops import SetOps
from .element._helpers.conversion import Conversion

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
        *args: Element,
    ):
        """
        Initialize a Group instance.

        Args:
            share (ShareEntity | str, optional): The share code or entity associated with the group.
            *args: Elements to initialize the group with.
        """
        # Initialize Cayley table with NoneElement for all Elements
        cayleyTable = {}
        for iType in Element.__subclasses__():
            if iType != elements.NoneElement: 
                cayleyTable[iType] = elements.NoneElement()
        self._cayleyTable = cayleyTable

        # Update Cayley table with provided elements
        self.updateCayleyTableWithGroupElements(*args)

        # Set the share entity
        self._shareEntity = ShareEntity.createShareEntity(share)

    def __str__(self):
        selfStr =  f'share:{self._shareCode}'
        for subclass in Element.__subclasses__(): 
            if self._cayleyTable.get(subclass,False):
                selfStr += f"""\n{subclass} have {len(self._getElement(subclass).dataPoints)} Data"""
            else: 
                selfStr+=f"""\n{subclass} is empty"""
        return selfStr
        


    @property
    def _shareCode(self) -> str:
        return self._shareEntity.shareCode


    

    @property
    def _valuedSubgroup(self) -> dict[type[Element], Element]:
        """
        Get the valued subgroup of the group.

        Returns:
            dict: A dictionary of element types and their corresponding group elements
                  that are not NoneElement.
        """
        valuedCayleyTable = dict()
        for iClass, iEle in self._cayleyTable.items():
            if iEle:
                valuedCayleyTable[iClass] = iEle
        return valuedCayleyTable
    
    
    
    class _ElementCheck: 
        def __init__(
            self,
            generatedElement:set[type[Element]],
            registry:dict[type[Element],tuple[set[type[Element]]]]
            ):
            self._genEle = generatedElement
            self._registry = registry

        @property
        def complete(self)->bool: 
            return len(self.registry) == 0 
                
        @property
        def genEle(self)->set[type[Element]]: 
            return self._genEle
        
        @property
        def notGened(self)->set[type[Element]]: 
            return set(self.registry.keys()).difference(self.genEle)
        
        @property
        def registry(self)->dict[type[Element],tuple[set[type[Element]]]]: 
            return self._registry
        
        
        def updateGenerated(self,ele:type[Element]): 
            self._genEle.add(ele)
        
        
    
    def update(self,ec:_ElementCheck|None=None):      
        if ec is None:
            #set ElementCheck
            ##By getting a copy of the Registry
            _copyReg = dict()            
            for iKey in Registry.getSet().difference(self._valuedSubgroup):
                _copyReg[iKey] = Registry.getRequirements(iKey)
            ec = self._ElementCheck(set(self._valuedSubgroup.keys()),_copyReg)
        elif ec.complete:
            return 
        localLoop = ec.notGened
        for iClass in localLoop:
            
            requirementsForI = ec.registry[iClass]
            #Found if anyone of the requirement is able to met 
            for req in requirementsForI:                 
                if req.issubset(ec.genEle): 
                    #generate iClass in Cayley Table and update the genEle in ELementCheck
                    genedEle = self._getElement(iClass)
                    if genedEle: 
                        self.setCayleyElement(genedEle)
                    else: 
                        raise(ValueError(f"Fail to generate {iClass} for unknown reason"))
                    ec.updateGenerated(iClass)
                    self.update(ec)
                    

            
            
            
        
        
    
    
 
    
                
        
        
    
    def setCayleyElement(self,ele: Element): 
        if not isinstance(ele,Element): 
            raise TypeError(f"""{ele} is of type{type(ele)}
                            but not {Element}""")
        if isinstance(ele,elements.NoneElement): 
            print(f"""Warning class {type(ele)} to None
                  in cayleyElement of {self._shareCode}""")
            return None
        
        self._cayleyTable[type(ele)] = ele

    def updateCayleyTableWithGroupElements(self, *args: Element):
        """
        Update the Cayley table with the provided elements.

        Args:
            *args: Elements to add to the Cayley table.
        """
        
        for iArg in args:
            self.setCayleyElement(iArg)



    def _getElement(
        self,
        eleTemplate: Element|type[Element]
    ) -> Element:
        """
        Retrieve an element of the specified class from the Cayley table if existed
        else generate the element if possible.

        Args:
            eleTemplate (element.Element|type[element.Element]): The element to retrieve.

        Returns:
            element.Element: The retrieved element.

        Raises:
            TypeError: If the provided class is not a subclass of element.Element.
            ValueError: If the element class cannot be resolved for the group.
        """
        
        if isinstance(eleTemplate,type):
            if issubclass(eleTemplate,Element):
                eleClass = eleTemplate
        elif isinstance(eleTemplate,Element): 
            eleClass = type(eleTemplate)
        else: 
            raise TypeError("")    
        
            
        # Check if the element exists in the valued subgroup
        if eleClass in self._valuedSubgroup:
            return self._cayleyTable[eleClass]

        # Attempt to find convertible classes
        convertibleClasses = Conversion.getElementClassesThatCanConvertBy(eleClass)
        if convertibleClasses:
            for conClass in convertibleClasses:
                if self._cayleyTable.get(conClass,False):
                    self._cayleyTable:dict[type[Element],Element]
                    resultElement = self._cayleyTable.get(conClass).convertTo(eleTemplate)
                    #self.setCayleyElement(resultElement)
                    return resultElement
        # Attempt to resolve using an operator
        targetOperator = _operator.Operator.getOperatorforTargetClass(eleClass)
        if targetOperator:
            for signature in targetOperator.getSignatures():
                if signature and signature.issubset(self._valuedSubgroup):
                    operands = [self._cayleyTable[sig] for sig in signature]
                    resultElement = targetOperator.dot(*operands)
                    #self.setCayleyElement(resultElement)
                    return resultElement

        # If no resolution is possible, return NoneElement
        return elements.NoneElement()
    



        


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
        for key, value in groupB._cayleyTable.items():
            if value and key not in self._valuedSubgroup:
                elementsToBeUpdates.append(value)
        self.updateCayleyTableWithGroupElements(*elementsToBeUpdates)
        
    def acceptVisitor(self,v): 
        for iClass,iEle in self._valuedSubgroup.items(): 
            iEle.visitorHandler.acceptVisitor(v)
    
    def acceptOutVisitor(self, v, destDir:str):
        import os
        destDir = os.path.splitext(destDir)[0]
        os.makedirs(destDir, exist_ok=True)
        for iClass, iEle in self._valuedSubgroup.items():
            destVar = os.path.join(destDir, iClass.__name__)
            iEle.visitorHandler.acceptOutVisitor(v, destVar)
    
    @classmethod
    def normalizeAllGroups(
        cls,
        *args:Group,
        updateBeforeNormalize:bool = False,        
    ):   
                
        groups: list[Group] = list(args)
        if len(groups) < 2:
            raise ValueError("At least two groups are required for normalization.")

        if updateBeforeNormalize: 
            for iGroup in groups: 
                iGroup.update()

        firstGroup = groups[0]
                    
        
        commonElement = set(
            firstGroup._valuedSubgroup.keys()
        )
        
        
        for iGroup in groups[1:]:
            commonElement.intersection_update(iGroup._valuedSubgroup.keys())
        
        
        for iClass in commonElement:            
            goodElements = SetOps.intersectMany(*[x._getElement(iClass) for x in groups])
            
            
            for j,jGroup in enumerate(groups):
                jGroup._cayleyTable[iClass] = goodElements[j]

    





