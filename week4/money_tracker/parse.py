import re
import constants
import datetime
import itertools
from simple_database import Database

def read_database_from_file(filename):
    # if it is not possible to parse the contents of
    # the file named @filename to a database, a ValueError is raised
    with open(filename) as f:
        lines = f.readlines()
    return parse_lines(lines)

def parse_lines(lines):
    # returns the user_data corresponding to @lines
    # if the first line is not a date line, a ValueError is raised
    # if parsing a line from @lines is not a date line or a data line, a ValueError is raised
    
    date_line_pattern = re.compile(r'\s*===\s*(.+)\s*===')
    data_line_pattern = re.compile(r'\s*(.+)\s*,\s*(.+)\s*,\s*({inc_str}|{exp_str})'
                                   .format(inc_str=constants.INCOME_STR, exp_str=constants.EXPENSE_STR))
    
    def parse_line(line):
        # if @line is a date line, returns ('date', <date>), where <date> is the
        # date extracted from @line.
        # else if @line is a data line, deturns ('data', <amount>, <category>, <type>),
        # where <amount>, <category>, <type> are extracted from @line
        # if parsing is not possible, a ValueError will be raised

        date_match = date_line_pattern.match(line)
        if date_match:
            date_str = date_match.group(1)
            return ('date', parse_date(date_str))
        
        data_match = data_line_pattern.match(line)
        if data_match:
            amount_str, category_str, _type_str = data_match.group(1, 2, 3)
            amount = parse_amount(amount_str)
            category = parse_category(category_str)
            _type = parse_type(_type_str)
            return ('data', amount, category, _type)

        raise ValueError('the line is neither a data line nor a date line')
    
    try:
        first_parsed = parse_line(lines[0])
    except ValueError:
        raise ValueError(f'unable to parse the first line')

    if first_parsed[0] != 'date':
        raise ValueError(f'the first line must be a date')
        
    current_date = first_parsed[1]
    tuples = []
    for line_num, line in enumerate(itertools.islice(lines, 1, len(lines)), start=2):
        try:
            parsed = parse_line(line)
        except ValueError:
            raise ValueError(f'unable to parse line {line_num}')
        if parsed[0] == 'date':
            current_date = parsed[1]
        else:
            amount, category, _type = parsed[1:]
            tuples.append((current_date, amount, category, _type))
    return Database(constants.COLUMN_NAMES, tuples)

def parse_amount(amount_str):
    # tries to convert @amount_str to a number
    # if not possible, a ValueError is raised
    
    for num_type in (int, float):
        try:
            val = num_type(amount_str)
        except ValueError:
            continue
        if val >= 0:
            return val
    raise ValueError

def write_database_to_file(db, filename):
    with open(filename, 'w') as f:
        f.write(db_to_str(db))
        f.write('\n')

def parse_date(date_str):
    # if @date_str cannot be parsed to a date, a ValueError is raised
    date_pattern = re.compile(r'(\d+)-(\d+)-(\d+)')
    m = date_pattern.match(date_str)
    if not m:
        raise ValueError(f'invalid date format: "{date_str}"')
    day, month, year = map(int, m.group(1, 2, 3))
    return datetime.date(year, month, day)

def date_to_str(date):
    # parse_date(date_to_str(date)) == date must be true
    return f'{date.day}-{date.month}-{date.year}'

def date_to_output_str(date):
    return f'=== {date_to_str(date)} ==='

def parse_category(category_str):
    if not category_str:
        raise ValueError('the empty string cannot be a category')
    return category_str

def parse_type(type_str):
    if type_str not in (constants.INCOME_STR, constants.EXPENSE_STR):
        raise ValueError(f'unable to parse "{type_str}" to a type: '
                         f'it must be one of {str({constants.INCOME_STR, constants.EXPENSE_STR})}')
    return type_str

def read_date_from_stdin():
    # tries to read a date from stdin until a valid format is entered
    # if an invalid format is entered, an error message is displayed
    # and the user is asked to try again.
    while True:
        try:
            date_str = input(constants.PROMPT)
            return parse_date(date_str)
        except ValueError:
            print(f'"{date_str}" is not a valid date. try again:')

def read_category_from_stdin():
    # tries to read a category until a valid one is entered
    # if an invalid one is entered, an error message is displayed
    # and the user is asked to try again
    while True:
        category = input(constants.PROMPT)
        if not category:
            print('please enter a nonempty string')
        else:
            return category

def read_amount_from_stdin():
    # tries to read a number from stdin until a valid one is entered
    # if an invalid number is entered, an error message is displayed
    # and the user is asked to try again
    while True:
        amount_str = input(constants.PROMPT)
        try:
            return parse_amount(amount_str)
        except ValueError:
            print(f'"{amount_str}" is not a valid amount. try again:')


def db_to_str(db):
    records = db.query(sort_by={'date'})
    if not records:
        return ''
    current_date = records[0][0]
    lines = [date_to_output_str(current_date)]
    for record in records:
        date, amount, category, _type = record
        if date != current_date:
            current_date = date
            lines.append(date_to_output_str(date))
        lines.append(f'{amount}, {category}, {_type}')
    return '\n'.join(lines)
