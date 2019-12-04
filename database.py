"""
db.set( { key:value }, path_1, path_2, ..., path_n, append=T/F )
db.get( path_1, path_2, ..., path_n )
"""


class DBKeyError(KeyError):
    """
    Raise when the key isn't a string.
    """
    def __init__(self, *args, **kwargs):
        KeyError.__init__(self, *args, **kwargs)

class DBTypeError(TypeError):
    """
    Raise when the type isn't a dict.
    """
    def __init__(self, *args, **kwargs):
        TypeError.__init__(self, *args, **kwargs)


class db(object):
    def __init__(self):
        self.dat = {}

    def set(self, item, *args, append=False):
        """
        Set the value at the key path to the item.
        If append is True, add dict item to dict at key path.
        """

        if type(item) == dict:
            try:
                for k in item.keys():
                    if type(k) != str:
                        raise DBTypeError
            except DBTypeError:
                print("key in item not a string.")
                return None
        
        retr = self.dat
        if len(args) == 1:
            try:
                if type(args[0]) != str:
                    raise DBKeyError
            except DBKeyError:
                print("Key must be a string.")
                return None
        elif len(args) == 0:
            print("No key given.")
            return None
        for arg in args[:-1]:
            try:
                if type(arg) != str:
                    raise DBKeyError
                retr = retr[arg]
            except DBKeyError:
                print("Key must be a string.")
                return None
            
            except KeyError:
                print("Key '", arg, " ' does not exist.")
                return None
                
        if append:
            try:
                if type(retr[args[-1]]) == dict and type(item) == dict:
                    retr = retr[args[-1]]
                    for k,v in item.items():
                        retr[k] = v
                else:
                    raise DBTypeError
                
            except DBTypeError:
                print("item or item at key path is not dict.")
                return None
                
            except KeyError:
                print("Key '", arg[-1], " ' does not exist.")
                return None
                        
        else:
            retr[args[-1]] = item
            
        return True
            

    def get(self, *args):
        """
        Get element at key path.
        """
        retr = self.dat
        for arg in args:
            try:
                if type(arg) != str:
                    raise DBKeyError
                retr = retr[arg]
                
            except DBKeyError:
                print("Key must be string.")
                return None
            
            except KeyError:
                print("Key '", arg, " ' does not exist.")
                return None
            
        return retr
                


