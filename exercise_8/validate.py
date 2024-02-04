from inspect import signature
from functools import wraps
class Validator:
    
    validators = { }
    def __init__(self,name=None):
        self.name = name
        
    def __set_name__(self,owner,name):
        self.name = name
    
    @classmethod
    def __init_subclass__(cls):
        cls.validators[cls.__name__] = cls
        
    @classmethod
    def check(cls,value):
        return value
    
    def __set__(self,instance,value):
        instance.__dict__[self.name] = self.check(value)
    
class Typed(Validator):
    expected_type = object
    @classmethod
    def check(cls,value):
        assert isinstance(value,cls.expected_type),f'Expected {cls.expected_type}'
        return super().check(value)
    
    
class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)

class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)

class Integer(Typed):
    expected_type = int

class Float(Typed):
    expected_type = float

class String(Typed):
    expected_type = str

class PositiveInteger(Integer, Positive):
    pass

class PositiveFloat(Float, Positive):
    pass

class NonEmptyString(String, NonEmpty):
    pass

class Stock:
    name   = String()
    shares = PositiveInteger()
    price  = PositiveFloat()

    def __init__(self,name,shares,price):
        self.name = name
        self.shares = shares
        self.price = price


def validated(func):
    sig = signature(func)
    annotations = dict(func.__annotations__)
    retcheck = annotations.pop('return',None)
    def wrapper(*args,**kwargs):
        bound = sig.bind(*args,**kwargs)
        error = []
        
        for name,validator in annotations.items():
            try:
                validator.check(bound.arguments[name])
            except Exception as e:
                    error.append(f'{name}:{e}')
        if error:
            raise TypeError('Invalid argument(s):'+','.join(error))
        
        result = func(*args,**kwargs)
        if retcheck:
            try:
                retcheck.check(result)
            except Exception as e:
                raise TypeError(f'Invalid return value:{e}')
            
        return result
    return wrapper

def enforce(*types,**kwtypes):
    def decorator(func):
        sig = signature(func)
        bound_types = sig.bind_partial(*types,**kwtypes).arguments
        retcheck = bound_types.pop('return_',None)
        @wraps(func)
        def wrapper(*args,**kwargs):
            errors = []
            bound_values = sig.bind(*args,**kwargs)
            for name,value in bound_values.arguments.items():
                if name in bound_types:
                    try:
                        bound_types[name].check(value)
                    except Exception as e:
                        errors.append(f'Argument {name} must be {bound_types[name]}')
            if errors:
                    raise TypeError(f'Invalid arguements' + ','.join(errors))
            
            result = func(*args,**kwargs)
            if retcheck:
                try:
                    retcheck.check(result)
                except Exception as e:
                    raise TypeError(f'Invalid return value:{e}')
            return result
        return wrapper
    return decorator


_typed_classes =[
    ('Integer',int),
    ('Float',float),
    ('String',str)
]
globals().update((name, type(name, (Typed,), {'expected_type':ty}))
                 for name, ty in _typed_classes)