class Database:
    def __init__(self, column_names, tuples):
        self.column_names = tuple(column_names)
        self.column_names_set = set(self.column_names)
        self.tuples = set(tuples)
    
    def query(self, condition=None, restrict_to=None, sort_by=None):
        if restrict_to is None:
            restrict_to = self.column_names_set
        else:
            self._verify_column_names(restrict_to, msg='restrict_to contains an invalid column name')
            
        self._verify_column_names(sort_by, msg='sort_by contains an invalid column name')
        
        restrict_to = self._get_indicies(restrict_to)
        filtered = (filter(condition, self.tuples) if condition is not None
                    else iter(self.tuples))
        if sort_by is None:
            return [_project(tup, restrict_to) for tup in filtered]
        else:
            sort_by = self._get_indicies(sort_by)
            return [_project(tup, restrict_to) for tup in sorted(filtered, key=lambda tup: _project(tup, sort_by))]

    def _verify_column_names(self, column_names, msg):
        # if @column_names is None, nothing happens
        # if a column in @column_names is not valid,
        # a ValueError will be raised with the message
        # @msg and an indication of the invalid column name
        
        if column_names is not None:
            for column_name in column_names:
                if column_name not in self.column_names_set:
                    raise ValueError(f'{msg}: "{column_name}"')
            
    def _get_indicies(self, column_names_set):
        return sorted(self.column_names.index(name) for name in column_names_set)
        
    def make_query_condition(self, predicate, column_names='all'):
        if column_names == 'all':
            column_names = self.column_names_set
        else:
            self._verify_column_names(column_names, 'column_names contains an invalid column name')
            
        indicies = self._get_indicies(column_names)
        return lambda tup: predicate(*_project(tup, indicies))
            
    def add_tuple(self, *tup):
        if len(tup) != len(self.column_names):
            raise ValueError(f'invalid length. expected {len(self.column_names)}, '
                             f'but was given {len(tup)} values')
        self.tuples.add(tup)

    def __str__(self):
        names_str = ' '.join(self.column_names)
        tuples_str = '\n'.join(map(str, self.tuples))
        return f'{names_str}\n{tuples_str}'
    
def _project(tup, indicies):
    return tuple(tup[i] for i in indicies)
