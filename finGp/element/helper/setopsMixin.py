from typing import TypeVar, Type, List
from ..base import Element

T = TypeVar('T', bound=Element)

class SetOpsMixin:
    
    def __init__(self,dataPoints,elementCls:Type): 
        self.dataPoints = dataPoints
        self.elementCls = elementCls
    
    def intersect(self: T, other: T) -> T:
        """
        Return a new instance containing only DataPoints present in both self and other.

        Args:
            other (SetOpsMixin): Another element to intersect with.

        Returns:
            SetOpsMixin: A new instance with intersected DataPoints.
        """
        # Build hash maps for fast lookup
        self_hashes = {hash(dp): dp for  dp in self.dataPoints}
        other_hashes = {hash(dp): dp for dp in other.dataPoints}
        common_hashes = set(self_hashes) & set(other_hashes)
        intersected_points = [self_hashes[h] for h in common_hashes]
        return self.elementCls(intersected_points)

    @staticmethod
    def intersectMany(*elements: T) -> List[T]:
        """
        Return a list of elements, where each element is the intersection of that element
        with all the others in the provided arguments.

        Args:
            *elements (SetOpsMixin): Two or more elements to intersect.

        Returns:
            List[SetOpsMixin]: A list of elements, each intersected with all others.

        Raises:
            ValueError: If fewer than two elements are provided.
        """
        if len(elements) < 2:
            raise ValueError("At least two Element instances are required for intersection.")

        result = []
        hash_maps = [{hash(dp): dp for dp in elem.dataPoints} for elem in elements]
        for idx, hash_map in enumerate(hash_maps):
            other_hash_maps = hash_maps[:idx] + hash_maps[idx+1:]
            common_hashes = set(hash_map.keys())
            for other_map in other_hash_maps:
                common_hashes &= set(other_map.keys())
            intersected_points = [hash_map[h] for h in common_hashes if hash_map[h].valid()]
            result.append(type(elements[idx])(intersected_points))
        return result