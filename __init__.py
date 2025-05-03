'''
The package provide a wrapper for a list of dataPoint of the 
same implementation type.  
Its sub-module 'dataPoint' handle the logic of what is comparable or the same
and handle the logic of valid data point. 

This module is intended to be used by the 'manipulationOfDataCollection' module.

This module provide a base for future development according to the needs of fiancial researcher

'''



from .financial_analysis.collectionGroup import CollectionGroup,GroupElement
from .creator import PricingCollectionCreator,NewsCollectionCreator,Creator


__all__ = [CollectionGroup,GroupElement,Creator,PricingCollectionCreator,NewsCollectionCreator]

