from ...visitorHandler import VisitorHandler

class CarNVisitorHandler(VisitorHandler):

    def __init__(self,element):         
        self.element = element
    
    def acceptVisitor(self,v):
        return v.visitCarNElement(self.element)
    
    
    def acceptOutVisitor(self,v, dest: str):
        return v.visitOutCarNElement(self.element, dest)