'''
Created on 16.10.2014

@author: trunneml
'''

def short_description(description, **kwargs):
    """
    This decorator adds the django short_description attribute to the
    given function.
    
    It also adds every keyword argument as extra attribute to the
    decorated function.
    """
    def _wrapper(func):
        func.short_description = description
        for key in kwargs:
            setattr(func, key, kwargs[key])
        return func
    return _wrapper

