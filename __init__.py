'''
The package provide a wrapper for a list of dataPoint of the 
same implementation type.  
Its sub-module 'dataPoint' handle the logic of what is comparable or the same
and handle the logic of valid data point. 

This module is intended to be used by the 'manipulationOfDataCollection' module.

This module provide a base for future development according to the needs of fiancial researcher

'''



from .shareEntity import ShareEntity
from .collection import DataCollection
from .creator import ConcreteCreatorPricingCollection,ConcreteCreatorNewsCollection,Creator
from point import CarNDataPoint,NoneDataPoint,DataPoint,NewsNewsDataPoint,HistoricalDataPoint

__all__ = [ShareEntity,DataCollection,Creator,ConcreteCreatorPricingCollection,ConcreteCreatorNewsCollection,DataPoint,CarNDataPoint,NoneDataPoint,NewsNewsDataPoint,HistoricalDataPoint]

