def typedproperty(name, expected_type):
    private_name = '_' + name

    @property
    def prop(self):
        return getattr(self, private_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(f'Expected {expected_type}')
        setattr(self, private_name, value)

    return prop

def String(name):
    return typedproperty(name,str)

def Integer(name):
    return typedproperty(name,int)

def Float(name):
    return typedproperty(name,float)
    

class typedpropertymeta:
    def __init__(self,type):
        self.type = type
        self.private_name = None
    def __set_name__(self,owner,name):
        self.private_name = '_' + name
    
    def __get__(self,instance,owner):
        if instance is None:
            return self
        return getattr(instance,self.private_name)
    def __set__(self,instance,value):
        if not isinstance(value,self.type):
            raise TypeError(f'Expected {self.type}')
        setattr(instance,self.private_name,value)

