class assertRaises:
    class WrongException(Exception):
        # raised when the context raises the wrong exception
        pass
    
    class NoException(Exception):
        # raised when the context does not raise an exception
        pass
    
    def __init__(self, exc_type_or_tuple, msg=None):
        # exc must be an Exception or a tuple of Exceptions
        if type(exc_type_or_tuple) is tuple:
            self.exc_types = exc_type_or_tuple
        else:
            # exc_type_or_tuple is an Exception
            self.exc_types = (exc_type_or_tuple,)

        self.msg = msg

    def __enter__(self):
        pass

    def __exit__(self, _type, value, traceback):
        if value is None:
            # no exception was raised during the execution of the block
            raise assertRaises.NoException(f'No exception was raised during the execution of the context')
        
        if _type not in self.exc_types:
            raise assertRaises.WrongException(f'wrong exception was raised: {_type}')

        if not value.args or value.args[0] != self.msg:
            raise assertRaises.WrongException(f"the exception's message was {value.args[0]}, "
                                              f'but expected {self.msg}')
        
        return True

if __name__ == '__main__':
    with assertRaises(KeyError):
        for k in range(1000000):
            pass
        print('doing something')
        for k in range(1000000):
            pass
        raise KeyError
