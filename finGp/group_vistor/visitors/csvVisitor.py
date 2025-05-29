import csv

from ..visitor import Visitor
from ... import element



    

class CsvVistor(Visitor):
        
    def visitCarNElement(
        self,
        cEle: element.Car3Element)->list[list[str]]:
        
        eleList = [["date", "previous_date", "follow_date", "cumulativeAbnormalReturn", "intervalN"]]
        for iCar in cEle.dataPoints:
            if iCar.valid():
                eleList.append([
                    str(iCar.date),
                    str(iCar.previousDate),
                    str(iCar.followingDate),
                    str(iCar.cumulativeAbnormalReturn),
                    str(iCar.intervalN)
                ])
                
        return eleList

    def visitNewsElement(
        self,
        nEle: element.NewsElement)->list[list[str]]:
        
        eleList = [["date", "siteAddress", "sentimentalScore"]]
        for iNews in nEle.dataPoints:
            if iNews.valid():
                eleList.append([
                    str(iNews.date),
                    iNews._siteAddress,
                    str(iNews.sentimentalScore)
                ])
        
        return eleList

    def visitNoneElement(
        self,
        nEle: element.NoneElement)->list:
        return []

    def visitPricingElement(
        self,
        pEle: element.PricingElement)->list[list[str]]:
        if not isinstance(pEle,element.PricingElement):
            if isinstance(pEle,element.NoneElement):
                return []
            else:
                raise TypeError(f"Input is not a PricingElement instance but {type[pEle]}")
        eleList = [["date", "adjusted_close"]]
        for iPrice in pEle.dataPoints:
            if iPrice.valid():
                eleList.append([
                    str(iPrice.date),
                    str(iPrice.adjClose)
                ])
                
        return eleList

    def visitCarsNewsElement(
        self,
        cN_ele: element.Car3NewsElement)->list[list[str]]:
        
        eleList = [["date", "previous_date", "follow_date", "cumulativeAbnormalReturn", "intervalN", "SentimentalScore"]]
        for iCar in cN_ele.dataPoints:
            if iCar.valid():
                eleList.append([
                    str(iCar.date),
                    str(iCar.carN.previousDate),
                    str(iCar.carN.followingDate),
                    str(iCar.carN.cumulativeAbnormalReturn),
                    str(iCar.carN.intervalN),
                    str(iCar.accumlatedSentimentalScore)
                ])
        
        return eleList





    def visitOutCarNElement(
        self,
        cEle,
        dest:str):
        
        if not dest.endswith('.csv'):
            dest = dest+'.csv'
        eleList = self.visitCarNElement(cEle)
        with open(dest, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(eleList)

    def visitOutNewsElement(
        self,
        nEle,
        dest:str):
        
        if not dest.endswith('.csv'):
            dest = dest+'.csv'
        eleList = self.visitNewsElement(nEle)
        with open(dest, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(eleList)



    def visitOutNoneElement(
        self,
        nEle,
        dest:str):
        if not dest.endswith('.csv'):
            dest = dest+'.csv'
        eleList = self.visitNoneElement(nEle)
        with open(dest, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(eleList)


    def visitOutPricingElement(
        self,
        pEle,
        dest:str):
        if not dest.endswith('.csv'):
            dest = dest+'.csv'
        eleList = self.visitPricingElement(pEle)
        with open(dest, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(eleList)


    def visitOutCarsNewsElement(
        self,
        cN_ele,
        dest:str):
        
        if not dest.endswith('.csv'):
            dest = dest+'.csv'
        eleList = self.visitCarsNewsElement(cN_ele)
        with open(dest, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(eleList)