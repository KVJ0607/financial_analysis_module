from ...visitorHandler import VisitorHandler

class CarNewsVisitorHandler(VisitorHandler):    
    
    def __init__(self,element):         
        self.element = element
    
    def acceptVisitor(self,v):
        return v.visitCarsNewsElement(self.element)  

    def acceptOutVisitor(
        self,
        v,
        dest:str): 
        return v.visitOutCarsNewsElement(self.element,dest)  