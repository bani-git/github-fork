
def singleton(theClass):
    """ Decorator for a class to make a singleton out of it """
    classInstances = {}

    def getInstance(*args, **kwargs):
        """ Create or get the existing instance """
        key = (theClass, args, str(kwargs))
        if key not in classInstances:
            classInstances[key] = theClass(*args, **kwargs)
        return classInstances[key]

    return getInstance
