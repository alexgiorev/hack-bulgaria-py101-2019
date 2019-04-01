import itertools
import re
import operator

class Database:
    def __init__(self, types, column_names, records):
        self.types = types
        self.column_names = column_names
        self.records = records
    
    def get_column_key(self, column_name):
        coli = self.column_index(column_name)
        if coli is None:
            raise ValueError(f'"{column_name}" is not a valid column name')
        return lambda record: record[coli]

    def column_index(self, column_name):
        try:
            return self.column_names.index(column_name)
        except ValueError:
            return None
        
    def has_column(self, column_name):
        return column_name in self.column_names
    
    def generate_all_records_satisfying(self, conditions):
        predicates = [self._make_predicate(condition) for condition in conditions]
        return (record for record in self.records if all(predicate(record) for predicate in predicates))
        
    def _make_predicate(self, condition):
        column_name, predicate, extra_arg = condition
        coli = self.column_index(column_name)
        if coli is None:
            raise ValueError(f'invalid column name in condition: {condition}')
        return lambda record: predicate(record[coli], extra_arg)
    
    def __str__(self):
        types_str = '({})'.format(', '.join(map(str, self.types)))
        column_names_str = '({})'.format(', '.join(self.column_names))
        records_string = '\n'.join(map(str, self.records))
        return f'{types_str}\n{column_names_str}\n{records_string}'
    
def filter_database(filename, order_by=None, **conditions_dict):
    database = parse_database_from_file(filename)
    conditions = parse_conditions_dict(conditions_dict)
    if order_by is None:
        return list(database.generate_all_records_satisfying(conditions))
    return sorted(database.generate_all_records_satisfying(conditions),
                  key=database.get_column_key(order_by))

def parse_conditions_dict(conditions_dict):
    names_to_predicates = {'contains': str.__contains__,
                           'startswith': str.startswith,
                           'gt': operator.gt,
                           'lt': operator.lt,
                           'eq': operator.eq}
    result = []
    for condition_str, extra_arg in conditions_dict.items():
        parts = condition_str.split('__', maxsplit=1)
        if len(parts) == 1:
            column_name, predicate_name = condition_str, 'eq'
        else:
            column_name, predicate_name = parts
        predicate = names_to_predicates.get(predicate_name)
        if predicate is None:
            raise ValueError(f'unable to parse the condition string "{condition_str}"; '
                             f'invalid predicate name: "{predicate_name}"')
        result.append((column_name, predicate, extra_arg))
    return result

def parse_database_from_file(filename):
    with open(filename) as f:
        lines = [line[:-1] for line in f.readlines() if not line.isspace()]
    if len(lines) < 2:
        raise ValueError(f'"{filename}" must have atleast 2 non-blank lines')
    column_types = parse_column_types(lines[0])
    column_names = tokenize_line(lines[1])
    number_of_columns = len(column_names)
    if len(column_types) != number_of_columns:
        raise ValueError(f'unable to parse {filename}: '
                         f'the number of types (given {len(column_types)}) '
                         f'must match the number of columns (given len(column_names))')
    records = []
    for line in itertools.islice(lines, 2, len(lines)):
        tokens = tokenize_line(line)
        if len(tokens) != number_of_columns:
            raise ValueError(f'unable to parse the line "{line}". it has {len(tokens)} tokens, but '
                             f'the number of columns is {number_of_columns}')
        records.append(tuple(data_type(token) for data_type, token in zip(column_types, tokens)))
    return Database(column_types, column_names, records)


def parse_column_types(line):
    type_names_to_converters = {'int': int, 'integer': int, 'string': str, 'str': str}    
    tokens = tokenize_line(line)
    result = []
    for token in tokens:
        converter = type_names_to_converters.get(token)
        if converter is None:
            raise ValueError(f'could not interpret the line "{line}" to a list of types: '
                             f'the token "{token}" is not a valid type name')
        result.append(converter)
    return result

def tokenize_line(line):
    if not line:
        raise ValueError('cannot tokenize the empty line')
    result = []
    current_token_chars = []
    in_double_quotes = False
    for char in line:
        if char == ',':
            if in_double_quotes:
                current_token_chars.append(char)
            else:
                result.append(''.join(current_token_chars))
                current_token_chars = []
        elif char == '"':
            in_double_quotes = not in_double_quotes
        else:
            current_token_chars.append(char)            
    if in_double_quotes:
        raise ValueError(f'could not parse the line "{line}". missing closing double quote')
    result.append(''.join(current_token_chars))
    return result

def first(*args, **kwargs):
    return filter_database(*args, **kwargs)[0]

def last(*args, **kwargs):
    return filter_database(*args, **kwargs)[-1]

def count(*args, **kwargs):
    return len(filter_database(*args, **kwargs))

def pl(l):
    for x in l:
        print(x)

