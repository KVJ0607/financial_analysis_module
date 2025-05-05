import json

from ..vistor import Vistor
import element_of_group
import csv

class CsvVistor(Vistor):
        
    def visitCarNElement(
        self,
        cEle: element_of_group.CarNElement)->list[list[str]]:
        
        eleList = [["date", "previous_date", "follow_date", "cumulativeAbnormalReturn", "intervalN"]]
        for iHash, iCar in cEle.inDict.items():
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
        nEle: element_of_group.NewsElement)->list[list[str]]:
        
        eleList = [["date", "siteAddress", "sentimentalScore"]]
        for iHash, iNews in nEle.inDict.items():
            if iNews.valid():
                eleList.append([
                    str(iNews.date),
                    iNews.__siteAddress,
                    str(iNews.sentimentalScore)
                ])
        
        return eleList

    def visitNoneElement(
        self,
        nEle: element_of_group.NoneElement)->list:
        return []

    def visitPricingElement(
        self,
        pEle: element_of_group.PricingElement)->list[list[str]]:
        
        eleList = [["date", "adjusted_close"]]
        for iHash, iPrice in pEle.inDict.items():
            if iPrice.valid():
                eleList.append([
                    str(iPrice.date),
                    str(iPrice.adjClose)
                ])
                
        return eleList

    def visitCarsNewsElement(
        self,
        cN_ele: element_of_group.CarsNewsElement)->list[list[str]]:
        
        eleList = [["date", "previous_date", "follow_date", "cumulativeAbnormalReturn", "intervalN", "SentimentalScore"]]
        for iHash, iCar in cN_ele.inDict.items():
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