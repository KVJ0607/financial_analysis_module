'''
The package provide a wrapper for a list of dataPoint of the 
same implementation type.  
Its sub-module 'dataPoint' handle the logic of what is comparable or the same
and handle the logic of valid data point. 

This module is intended to be used by the 'manipulationOfDataCollection' module.

This module provide a base for future development according to the needs of fiancial researcher

'''



#from .financial_analysis.collectionGroup import CollectionGroup
import group_operators
import group_creator 
import point 
from collectionGroup import CollectionGroup

import date_utils
from shareEntity import ShareEntity

__all__ = ["group_operators","group_creator","point","CollectionGroup","date_utils","ShareEntity"]

