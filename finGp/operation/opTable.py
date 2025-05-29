import inspect

from ..element import Element

from ..group.space import Space
from .. import operation

class OperationTable:
    """
    Represents a directed graph where each node is a key from spaceDefinition.
    """

    _SPACE = Space
    _OPERATION = dict()
    
    @classmethod
    def getSpaceDefinition(cls):
        return cls._SPACE.getSpaceDefinition()
    
    
    @classmethod
    def getDefaultOperationDefinition(cls):
        opTable = {}
        for name in dir(operation):
            obj = getattr(operation, name)
            if inspect.isclass(obj):
                if issubclass(obj, operation.Operator) and obj is not operation.Operator:
                    productClass = obj.getProductClass()
                    if productClass in cls._SPACE.getSpaceDefinition():
                        opTable[obj.getProductClass()] = TableMember(
                            productClass=obj.getProductClass(),
                            operator=obj,
                            operands=obj.getOperands()
                        )                        
        return opTable
    
    @classmethod
    def getOperationTable(cls)->dict[type[Element], 'TableMember']:
        if not cls._OPERATION:
            cls._OPERATION = cls.getDefaultOperationDefinition()
        return cls._OPERATION
    
    @classmethod
    def updateOperationTable(cls, operator:type[operation.Operator]):
        """
        Update the operation table with a new operator.
        
        Args:
            operator (type[operation.Operator]): The operator to be added.
        """
        if not issubclass(operator, operation.Operator):
            raise TypeError(f"{operator} is not a subclass of Operator.")
        
        productClass = operator.getProductClass()
        
        if productClass in cls._SPACE.getSpaceDefinition():
            cls._OPERATION[productClass] = TableMember(
                productClass=productClass,
                operator=operator,
                operands=operator.getOperands()
            )    
        else:
            raise ValueError(f"{productClass} is not in the space definition.")


class TableMember: 
    def __init__(self,productClass:type[Element], operator:type[operation.Operator],operands:set[type[Element]]):
        self._productClass = productClass
        self._operator = operator
        self._operands = operands
    
    def getOperator(self)->type[operation.Operator]:
        return self._operator
    
    def getOperands(self)->set[type[Element]]:
        return self._operands
    
    def getProductClass(self)->type[Element]:
        return self._productClass