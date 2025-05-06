import json

from ..vistor import Vistor
from ... import element_of_group

class JsonStrVistor(Vistor):
    
    def visitCarNElement(
        self,
        cEle:element_of_group.CarNElement)->str:
        eleList = []
        for iHash,iCar in cEle.inDict.items(): 
            if iCar.valid():
                eleList.append({
                'date':str(iCar.date),
                'previous_date':str(iCar.previousDate),
                'follow_date':str(iCar.followingDate),
                'cumulativeAbnormalReturn':str(iCar.cumulativeAbnormalReturn),
                'intervalN':str(iCar.intervalN)
                
                })
        
        return json.dumps(eleList)

            
              
    
    def visitNewsElement(
        self,
        nEle:element_of_group.NewsElement)->str:
        
        eleList = []
        for iHash,iNews in nEle.inDict.items():
            if iNews.valid():
                eleList.append({
                    'date':str(iNews.date),
                    'siteAddress':iNews.__siteAddress,
                    'sentimentalScore':str(iNews.sentimentalScore)
                })
        
        return json.dumps(eleList)
    

    
    def visitNoneElement(
        self,
        nEle:element_of_group.NoneElement)->str:
        return json.dumps({})
    
    
    def visitPricingElement(
        self,
        pEle:element_of_group.PricingElement)->str:
        
        eleList = []
        for iHash,iPrice in pEle.inDict.items():
            if iPrice.valid():
                eleList.append({
                    'date':str(iPrice.date),
                    'adjusted_close':str(iPrice.adjClose),
                })
                
        return json.dumps(eleList)
    
    def visitCarsNewsElement(
        self,
        cN_ele:element_of_group.CarNewsElement)->str:
        
        eleList = []
        for iHash,iCar in cN_ele.inDict.items(): 
            if iCar.valid():
                eleList.append({
                'date':str(iCar.date),
                'previous_date':str(iCar.carN.previousDate),
                'follow_date':str(iCar.carN.followingDate),
                'cumulativeAbnormalReturn':str(iCar.carN.cumulativeAbnormalReturn),
                'intervalN':str(iCar.carN.intervalN),
                'SentimentalScore':str(iCar.accumlatedSentimentalScore)                
                
                })
        
        return json.dumps(eleList)



    def visitOutCarNElement(self, cEle, dest):
        output = self.visitCarNElement(cEle)
        with open(dest, 'w') as file:
            file.write(output)
    
    def visitOutNewsElement(self, nEle, dest):
        output = self.visitNewsElement(nEle)
        with open(dest, 'w') as file:
            file.write(output)
    
    def visitOutNoneElement(self, nEle, dest):
        output = self.visitNoneElement(nEle)
        with open(dest, 'w') as file:
            file.write(output)
    
    def visitOutPricingElement(self, pEle, dest):
        output = self.visitPricingElement(pEle)
        with open(dest, 'w') as file:
            file.write(output)
    
    def visitOutCarsNewsElement(self, cN_ele, dest):
        output = self.visitCarsNewsElement(cN_ele)
        with open(dest, 'w') as file:
            file.write(output)
