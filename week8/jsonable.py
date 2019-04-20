import json

class Jsonable:
    PRIMITIVE_TYPES = {int: 'int', float: 'float', bool: 'bool',
                       str: 'str', type(None): 'NoneType'}
    
    def to_json_str(self, indent=4):
        # returns the json string corresponding to @self
        return json.dumps(self.to_json(), indent=indent)

    def to_json(self):
        # raises TypeError if it is not possible to transform @self to a json
        
        if type(self) in Jsonable.PRIMITIVE_TYPES:
            return {'object': self, 'type': Jsonable.PRIMITIVE_TYPES[type(self)]}
        elif type(self) is list:
            obj = list(map(Jsonable.to_json, self))
            return {'object': obj, 'type': 'list'}
        elif type(self) is dict:
            if not all(type(key) is str for key in self):
                raise ValueError(f'cannot convert the dict {self} to json: '
                                 'not all keys are strings')
            obj = {key: Jsonable.to_json(val) for key, val in self.items()}
            return {'object': obj, 'type': 'dict'}
        elif isinstance(self, Jsonable):
            _dict = {key: Jsonable.to_json(value) for key, value in self.__dict__.items()}
            return {'object': _dict, 'type': f'{type(self).__module__} {type(self).__name__}'}
        else:
            raise TypeError(f'objects of type {type(self)} cannot be converted to json')

        
    @staticmethod
    def from_json_str(json_str):
        # creates an instance of @cls based on the string @json_str
        return Jsonable.from_json(json.loads(json_str))


    @staticmethod
    def from_json(json):
        # creates an instance of @cls based on @json
        
        primitive_type_names = set(Jsonable.PRIMITIVE_TYPES.values())
        obj, _type = json['object'], json['type']

        if _type in primitive_type_names:
            return obj
        elif _type == 'list':
            return [Jsonable.from_json(subjson) for subjson in obj]
        elif _type == 'dict':
            return {key: Jsonable.from_json(val) for key, val in obj.items()}
        else:
            # _type is a string of the form "<module> <name>" which identifies a class
            cls = next((cls for cls in Jsonable.__subclasses__()
                        if [cls.__module__, cls.__name__] == _type.split()),
                       None)
            
            if cls is None:
                raise ValueError(f'unknown type: {_type}')

            result = object.__new__(cls)
            result.__dict__ = {key: Jsonable.from_json(val) for key, val in obj.items()}
            return result
