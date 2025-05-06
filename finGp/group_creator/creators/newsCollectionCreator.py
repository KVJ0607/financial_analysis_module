import csv

from ...date_utils import DateRepresentation
from ...element_of_group import NoneDataPoint, NewsDataPoint
from ...group import Group
from ...shareEntity import ShareEntity              


class NewsCollectionCreator:
    """
    A class to parse files and generate objects of type `Group` containing
    news data points. This class provides methods to handle different file
    formats, including CSV, and map their contents to structured data.
    """
    _enum = ['date', 'siteAddress', 'sentimentalScore']

    @classmethod
    def getInstacnefromCsv(
        cls,
        fileName: str,
        isHeading: bool = True,
        shareCode: str = '',
        dateIndex: int = 0,
        siteAddressIndex: int = 1,
        sentimentalScoreIndex: int = 2,
    ) -> Group:
        """
        Create a news collection group from a CSV file with detailed column mapping.

        Args:
            fileName (str): The path to the CSV file.
            isHeading (bool): Whether the CSV file contains a header row. Defaults to True.
            shareCode (str): The share code for the news data. Defaults to an empty string.
            dateIndex (int): The index of the date column. Defaults to 0.
            siteAddressIndex (int): The index of the site address column. Defaults to 1.
            sentimentalScoreIndex (int): The index of the sentimental score column. Defaults to 2.

        Returns:
            Group: A group containing news data points.
        """
        collections = []
        with open(fileName, mode='r') as infile:
            print(f"Reading {fileName}")
            reader = csv.reader(infile)
            keyList = cls._getKeyList(dateIndex, siteAddressIndex, sentimentalScoreIndex)
            if isHeading:
                next(reader)
            for row in reader:
                row_dict = dict(zip(keyList, row))
                date = row_dict.get(
                    cls._enum[0],
                    DateRepresentation.getNullInstance()
                )
                newsDataPoint = NewsDataPoint(
                    date,
                    row_dict.get(cls._enum[1], NoneDataPoint(date)),
                    row_dict.get(cls._enum[2], NoneDataPoint(date))
                )
                if newsDataPoint.valid():
                    collections.append(newsDataPoint)
                
        shareEntity = ShareEntity.createShareCode(shareCode)     
        return Group(shareEntity, NewsDataPoint.getGroupElement(collections))
    
    @classmethod
    def _getKeyList(
        cls,
        dateIndex: int,
        siteAddressIndex: int,
        sentimentalScoreIndex: int
    ) -> list:

        keyList = [0] * 3
        keyList[dateIndex] = cls._enum[0]
        keyList[siteAddressIndex] = cls._enum[1]
        keyList[sentimentalScoreIndex] = cls._enum[2]
        return keyList