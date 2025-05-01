class ReorderOperand:


    @classmethod
    def matchingOperand(cls,
                        gEleA,
                        gEleB,
                        leftType,
                        rightType)->tuple: 
        """
        All opertors are implictly non-communicative and are only defined for 
        a specified ordered. This method take two operands and return 
        them in a required oreder in a tuple.      
        """
        gEleAType = gEleA.pointType
        gEleBType = gEleB.pointType
        if gEleAType == leftType and gEleBType == rightType: 
            return gEleA,gEleB
        elif gEleBType == leftType and gEleAType == rightType: 
            return gEleB,gEleA
        else: 
            raise TypeError(f'''The two input should be of types {leftType} and {rightType}.
                            However, the arugments are of types {gEleAType} and {gEleBType}''')