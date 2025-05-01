'''
The package provide a wrapper for a list of dataPoint of the 
same implementation type.  
Its sub-module 'dataPoint' handle the logic of what is comparable or the same
and handle the logic of valid data point. 

This module is intended to be used by the 'manipulationOfDataCollection' module.

This module provide a base for future development according to the needs of fiancial researcher

'''



from .shareEntity import ShareEntity
from .financial_analysis.dataCollection import CollectionGroup
from .creator import PricingCollectionCreator,NewsCollectionCreator,Creator


__all__ = [ShareEntity,CollectionGroup,Creator,PricingCollectionCreator,NewsCollectionCreator]

