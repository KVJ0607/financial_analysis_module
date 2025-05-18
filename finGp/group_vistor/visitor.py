from abc import ABC,abstractmethod

class Visitor(ABC):
    
    @abstractmethod
    def visitCarNElement(self,cEle):
        pass 
    
    @abstractmethod
    def visitNewsElement(self,nEle):
        pass
    
    @abstractmethod
    def visitNoneElement(self,nEle):
        pass 
    
    @abstractmethod
    def visitPricingElement(self,pEle):
        pass 
    
    @abstractmethod
    def visitCarsNewsElement(self,cN_ele):
        pass 



    @abstractmethod
    def visitOutCarNElement(self,cEle,dest):
        pass 
    
    @abstractmethod
    def visitOutNewsElement(self,nEle,dest):
        pass
    
    @abstractmethod
    def visitOutNoneElement(self,nEle,dest):
        pass 
    
    @abstractmethod
    def visitOutPricingElement(self,pEle,dest):
        pass 
    
    @abstractmethod
    def visitOutCarsNewsElement(self,cN_ele,dest):
        pass 
