'''
This package mainly serve ..dataCollection.DataCollection class. 
The interface DataPoint represent a smallest atomic point of data. 


The main purpose of each implementation class is to: 

1. Act as a wrapper of the json-like data of the corresponding type. 

We may get the data from different sources or API. 
This class help to abstract different data sources and API.


2. Define what are the core attributes and thus provide a method to 
determine if a data point is valid or not 


3. Provide a hashing functions from atomic data point 
to a coordinate. It helps determination of 'comparable' 
or 'same' points.

Different class of data point has its statical logic of what points
are the same; for example a market price data point of the same 
date should considered the 'same' point if it belongs to the 
same company or 'comparable' point if it belongs to different 
company.

'''


from .dataPoint import DataPoint
from .point_imp.carNDataPoint import CarNDataPoint
from .point_imp.historicalDataPoint import HistoricalDataPoint,PricingDataPoint,AdjClosedDataPoint,NewsNewsDataPoint
from .point_imp.NoneDataPoint import NoneDataPoint


__all__ = [DataPoint,CarNDataPoint,HistoricalDataPoint,NoneDataPoint,PricingDataPoint,AdjClosedDataPoint,NewsNewsDataPoint]