from ...visitorHandler import VisitorHandler

class PricingVisitorHandler(VisitorHandler):

    def __init__(self,element):         
        self.element = element
            
    def acceptVisitor(self,v):
        return v.visitPricingElement(self.element)    

    def acceptOutVisitor(
        self,
        v,
        dest:str): 
        return v.visitOutPricingElement(self.element,dest)
    
    