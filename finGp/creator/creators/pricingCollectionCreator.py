import csv

from ...date_utils import DateRepresentation
from ...element import NoneDataPoint, PricingDataPoint
from ...group import Group
from ...shareEntity import ShareEntity


class PricingCollectionCreator:

    """
    A class to parse files and generate objects of type `Group` containing
    pricing data points. This class provides methods to handle different file
    formats, including CSV, and map their contents to structured data.
    """    
    _enum = ['date', 'open', 'high', 'low', 'close', 'adjClose', 'volume']


    @classmethod
    def getInstacnefromCsv(
        cls,
        fileName: str,
        isHeading: bool = True,
        shareCode: str = '',
        dateIndex: int = 0,
        openIndex: int = 1,
        highIndex: int = 2,
        lowIndex: int = 3,
        closeIndex: int = 4,
        AdjCloseIndex: int = 5,
        volumnIndex: int = 6,
    ) -> Group:
        """
        Create a pricing collection group from a CSV file with detailed column mapping.

        Args:
            fileName (str): The path to the CSV file.
            isHeading (bool): Whether the CSV file contains a header row. Defaults to True.
            shareCode (str): The share code for the pricing data. Defaults to an empty string.
            dateIndex (int): The index of the date column. Defaults to 0.
            openIndex (int): The index of the open price column. Defaults to 1.
            highIndex (int): The index of the high price column. Defaults to 2.
            lowIndex (int): The index of the low price column. Defaults to 3.
            closeIndex (int): The index of the close price column. Defaults to 4.
            AdjCloseIndex (int): The index of the adjusted close price column. Defaults to 5.
            volumnIndex (int): The index of the volume column. Defaults to 6.

        Returns:
            Group: A group containing pricing data points.
        """
        collections = []
        with open(fileName, mode='r') as infile:
            print(f"Reading {fileName}")
            reader = csv.reader(infile)
            keyList = cls._getKeyList(
                dateIndex, openIndex, highIndex, lowIndex, closeIndex, AdjCloseIndex, volumnIndex
            )
            if isHeading:
                next(reader)
            for row in reader:
                row_dict = dict(zip(keyList, row))
                date = row_dict.get(cls._enum[0], DateRepresentation.getNullInstance())

                newDataPoint = PricingDataPoint(
                    date,
                    row_dict.get(cls._enum[1], NoneDataPoint(date)),
                    row_dict.get(cls._enum[2], NoneDataPoint(date)),
                    row_dict.get(cls._enum[3], NoneDataPoint(date)),
                    row_dict.get(cls._enum[4], NoneDataPoint(date)),
                    row_dict.get(cls._enum[5], NoneDataPoint(date)),
                    row_dict.get(cls._enum[6], NoneDataPoint(date)),
                )

                if newDataPoint.valid():
                    collections.append(newDataPoint)
        shareEntity = ShareEntity.createShareEntity(shareCode)
        return Group(shareEntity, PricingDataPoint.getGroupElement(collections))

    @classmethod
    def _getKeyList(
        cls,
        dateIndex: int,
        openIndex: int,
        highIndex: int,
        lowIndex: int,
        closeIndex: int,
        AdjCloseIndex: int,
        volumnIndex: int,
    ) -> list[str]:
        
        keyList = [''] * 7
        keyList[dateIndex] = cls._enum[0]
        keyList[openIndex] = cls._enum[1]
        keyList[highIndex] = cls._enum[2]
        keyList[lowIndex] = cls._enum[3]
        keyList[closeIndex] = cls._enum[4]
        keyList[AdjCloseIndex] = cls._enum[5]
        keyList[volumnIndex] = cls._enum[6]
        return keyList

