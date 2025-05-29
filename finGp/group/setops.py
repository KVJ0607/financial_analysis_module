from ..element.base import Element,DataPoint
from typing import TypeVar

E = TypeVar("E", bound="Element")

class SetOps:
    
    def __init__(self,element:E): 
        self.element = element
    
    def index(self) -> dict[int,DataPoint]: 
        indexedEle = dict() 
        for iPoint in self.element.dataPoints: 
            indexedEle[hash(iPoint)] = iPoint
        return indexedEle
    
    def intersect(self, other: E) -> E:
        """
        Return a new instance containing only DataPoints present in both self and other.

        Args:
            other (SetOpsMixin): Another element to intersect with.

        Returns:
            SetOpsMixin: A new instance with intersected DataPoints.
        """
        # Build hash maps for fast lookup
        self_hashes = {hash(dp): dp for  dp in self.element.dataPoints}
        other_hashes = {hash(dp): dp for dp in other.dataPoints}
        common_hashes = set(self_hashes) & set(other_hashes)
        intersected_points = [self_hashes[h] for h in common_hashes]
        return type(self.element)(intersected_points)

    @staticmethod
    def intersectMany(*elements: E) -> list[E]:
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
        hashMaps = [{hash(dp): dp for dp in elem.dataPoints} for elem in elements]
            
        for idx, hash_map in enumerate(hashMaps):
            other_hash_maps = hashMaps[:idx] + hashMaps[idx+1:]
            common_hashes = set(hash_map.keys())
            for other_map in other_hash_maps:
                common_hashes &= set(other_map.keys())

            intersected_points = [hash_map[h] for h in common_hashes]
            result.append(type(elements[idx])(intersected_points))
        return result