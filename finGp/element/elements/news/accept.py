from ...visitorHandler import VisitorHandler
class NewsVisitorHandler(VisitorHandler):

    def __init__(self,element):         
        self.element = element
            
    def acceptVisitor(self,v):
        return v.visitNewsElement(self.element)
    
    def acceptOutVisitor(
        self,
        v,
        dest:str): 
        return v.visitOutNewsElement(self.element,dest)