from collections import defaultdict

from ...base import Element


    





class _ElementRequirement:
    def __init__(self, requirement: set[type[Element]]):
        if not isinstance(requirement, set):
            raise TypeError("requirement must be a set of types")
        for req in requirement:
            if not isinstance(req, type):
                raise TypeError("All elements in requirement must be types")
        self.requirement = requirement

    def __repr__(self):
        return f"ElementRequirements({self.requirement})"

    def getSet(self): 
        return self.requirement
    
class Registry:
    """
    Simple registry for storing and retrieving objects by name.
    """

    _registry:dict[Element,list[_ElementRequirement]] = defaultdict(list)


    @classmethod
    def register(cls, objType: type[Element]):
        cls._registry[objType] = []

    @classmethod
    def getRequirements(cls,objType:type[Element])->tuple[set[type]]: 
        return tuple([x.getSet() for x in cls._registry[objType] if x ])
    
    @classmethod
    def update(cls,objType: type[Element],eleReq:_ElementRequirement):
        cls._registry[objType].append(eleReq)

    @classmethod
    def registered(cls, obj_type: type) -> bool:
        """Check if a type is registered."""
        return obj_type in cls._registry.keys()

    @classmethod
    def unregister(cls, obj_type: type):
        if obj_type in cls._registry:
            del cls._registry[obj_type]
        else:
            return

    @classmethod
    def getSet(cls):
        """
        Return a set of non-generator elements
        """
        return set(cls._registry.keys())
    

    
    @staticmethod
    def makeElementRequirements(requirements: set[type[Element]]) -> _ElementRequirement:
        """
        Create an ElementRequirements instance.
        """
        return _ElementRequirement(requirements)    


