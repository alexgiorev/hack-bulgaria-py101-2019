import itertools 
import sys
import re

# for each part of an entry, the index at which it appears in the entry
DATE_INDEX = 0
AMOUNT_INDEX = 1
CATEGORY_INDEX = 2
TYPE_INDEX = 3

EXPENSE_STR = 'New Expense'
INCOME_STR = 'New Income'

def extract_parts_from_entry(entry, parts):
    # parts can be a tuple or a str. if it is a tuple, it's elements must be from {'date', 'amount', 'category', 'type'}
    # in that case, it returns a tuple, whose ith element is the part of entry corresponding to the word in parts[i]
    # for example, if @entry is ('20-03-1997', 10, 'food', 'expense') and @parts is ('date', 'date', 'type', 'amount', 'amount'),
    # the return value is ('20-03-1997', '20-03-1997', 'expense', 10, 10)
    # if @parts is (), () is returned
    # if parts is a str, it can be one of {'date', 'amount', 'category', 'type'}. in that case, only the relevant part is returned
    
    s2i = {'date': DATE_INDEX, 'amount': AMOUNT_INDEX, 'category': CATEGORY_INDEX, 'type': TYPE_INDEX}
    if type(parts) is tuple:
        parts_indexes = tuple(s2i[part] for part in parts)
        return tuple(entry[i] for i in parts_indexes)
    elif type(parts) is str:
        return entry[s2i[parts]]

def get_entries(user_data):
    # returns an iterator, which yields all entries from user_data
    for date, inc_exp in user_data.items():
        for amount, category in inc_exp['income']:
            yield (date, amount, category, 'income')
        for amount, category in inc_exp['expense']:
            yield (date, amount, category, 'expense')

def list_user_data(all_user_data):
    # returns a list containing all of the entries
    # in the sequence all_user_data
    return list(get_entries(all_user_data))

def get_income_entries(user_data):
    # returns an iterator of all income entries of @user_data
    for date, inc_exp in user_data.items():
        for amount, category in inc_exp['income']:
            yield (date, amount, category, 'income')

def get_incomes(user_data, parts=('amount', 'category')):
    return extract_parts_from_entries(get_income_entries(user_data, parts))

def extract_parts_from_entries(entries, parts):
    return (extract_parts_from_entry(entry, parts) for entry in entries)

def get_expense_entries(user_data):
    # returns an iterator of all expense entries of @user_data
    for date, inc_exp in user_data.items():
        for amount, category in inc_exp['expense']:
            yield (date, amount, category, 'expense')

def get_expenses(user_data, parts=('amount', 'category')):
    return extract_parts_from_entries(get_expense_entries(user_data), parts)
            
def show_user_incomes(all_user_data, parts=('amount', 'category')):
    return sorted(get_incomes(all_user_data, parts))

def show_user_savings(all_user_data, parts=('date', 'amount')):
    return [extract_parts_from_entry(income_entry, parts) for income_entry in get_income_entries(all_user_data)
            if income_entry[CATEGORY_INDEX] == 'Savings']

def show_user_deposits(all_user_data, parts=('date', 'amount')):
    return [extract_parts_from_entry(expense_entry, parts) for expense_entry in get_expense_entries(all_user_data)
            if expense_entry[CATEGORY_INDEX] == 'Deposit']

def show_user_expenses(all_user_data, parts=('amount', 'category')):
    return sorted(get_expenses(all_user_data, parts))

def list_user_expenses_ordered_by_categories(all_user_data):
    return sorted(get_expenses(all_user_data), key=lambda expense: expense[1])

def get_entries_at_date(user_data, date, parts=('amount', 'category', 'type')):    
    if date not in user_data:
        return None
    
    incomes_list = user_data[date]['income']
    income_entries = ((date, amount, category, 'income') for amount, category in incomes_list)

    expenses_list = user_data[date]['expense']
    expense_entries = ((date, amount, category, 'expense') for amount, category in expenses_list)
    
    return extract_parts_from_entries(itertools.chain(income_entries, expense_entries), parts)
    
    
def show_user_data_per_date(date, all_user_data):
    return [(amount, category, EXPENSE_STR if _type == 'expense' else INCOME_STR)
            for amount, category, _type in get_entries_at_date(all_user_data, date)]
            
def list_income_categories(all_user_data):
    return sorted(set(get_incomes(all_user_data, 'category')))

def list_expense_categories(all_user_data):
    return sorted(set(get_expenses(all_user_data, 'category')))

def add_income(income_category, amount, date, all_user_data):
    date_data = all_user_data.setdefault(date, {'income': [], 'expense': []})
    date_data['income'].append((amount, income_category))

def add_expense(expense_category, amount, date, all_user_data):
    date_data = all_user_data.setdefault(date, {'income': [], 'expense': []})
    date_data['expense'].append((amount, expense_category))
    
def read_user_data_from_file(filename):
    with open(filename) as f:
        return parse_lines(f.readlines())

def user_data_to_str(user_data):
    lines = []
    for date in user_data:
        lines.append(f'=== {date} ===')
        for amount, category, _type in get_entries_at_date(user_data, date):
            amount_str = str(amount)
            type_str = INCOME_STR if _type == 'income' else EXPENSE_STR
            lines.append(f'{amount_str}, {category}, {type_str}')
    return '\n'.join(lines)
    
def parse_lines(lines):
    # returns the user_data corresponding to @lines
    # if the first line is not a date line, a ValueError is raised
    # if parsing a line from @lines is not a date line or a data line, a ValueError is raised
    
    date_line_pattern = re.compile(r'===\s*(\d\d-\d\d-\d\d\d\d)\s*===')
    data_line_pattern = re.compile(r'\s*(.+)\s*,\s*(.+)\s*,\s*({inc_str}|{exp_str})'.format(inc_str=INCOME_STR, exp_str=EXPENSE_STR))
    
    def parse_line(line):
        # if @line is a date line, returns ('date', <date>), where <date> is the
        # date extracted from @line.
        # else if @line is a data line, deturns ('data', <amount>, <category>, <type>),
        # where <amount>, <category>, <type> are extracted from @line
        # else return None
        
        if line[0] == '=':
            match = date_line_pattern.match(line)
            if match:
                return ('date', match.group(1))
            return None
        else:
            match = data_line_pattern.match(line)
            if match:
                amount, category, _type = match.group(1, 2, 3)
                
                amount = parse_amount(amount)
                if amount is None:
                    return None
                
                _type = parse_type(_type)
                if type is None:
                    return None
                
                return ('data', amount, category, _type)
            return None

    def parse_type(_type):
        # tries to convert _type to 'income' or 'expense'
        # returns None if not possible
        return 'income' if _type == INCOME_STR else 'expense' if _type == EXPENSE_STR else None
        
    out = {}
    lines_iter = iter(lines)
    
    try: # parse the first line
        current = parse_line(next(lines_iter))
    except StopIteration: # when lines is empty
        return {}
    
    if current is None:
        raise ValueError('unable to parse first line')
    elif current[0] != 'date':
        raise ValueError('first line must be a date')
    
    current_date = current[1]
    out[current_date] = {'income': [], 'expense': []}
    for line_num, line in enumerate(lines_iter, start=2):
        parsed = parse_line(line)
        if parsed is None:
            raise ValueError(f'unable to parse line {line_num}')
        elif parsed[0] == 'date':
            current_date = parsed[1]
            out.setdefault(current_date, {'income': [], 'expense': []})
        else:
            amount, category, _type = parsed[1:]
            out[current_date][_type].append((amount, category))
    return out

def parse_amount(amount_str):
    # tries to convert @amount_str to a number
    # if not possible, None is returned
    for num_type in (int, float):
        try:
            val = num_type(amount_str)
        except ValueError:
            continue
        if val >= 0:
            return val
    return None

def write_user_data_to_file(user_data, filename):
    with open(filename, 'w') as f:
        f.write(user_data_to_str(user_data))
        f.write('\n')

def read_date_from_stdin(msg):
    print(msg)
    while True:
        date = input('>>> ')
        if not re.match(r'\s*\d\d-\d\d-\d\d\d\d\s*$', date):
            print(f'"{date}" is not a valid date.')
        else:
            return date

def read_amount_from_stdin(msg):
    print(msg)
    while True:
        amount_str = input('>>> ')
        amount = parse_amount(amount_str)
        if amount is None:
            print('invalid amount;')
        else:
            return amount

def read_category_from_stdin(msg):
    print(msg)
    while True:
        category = input('>>> ')
        if not category:
            print('please enter a nonempty string')
        else:
            return category

def repl(user_data):
    def show_all_data():
        print(user_data_to_str(user_data))

    def quit_on_eof(handler):
        def result():
            try:
                handler()
            except EOFError:
                pass
        return result

    @quit_on_eof
    def show_data_for_specific_date():
        # after this loop, the variable date will be a valid date
        while True:
            date = read_date_from_stdin('Enter date:')
            if date not in user_data:
                print(f'"{date}" is not in the database')
            else:
                break
                
        lines = [f'{amount}, {category}, {_type}' for amount, category, _type in show_user_data_per_date(date, user_data)]
        print('\n'.join(lines))

    def show_expenses_ordered_by_categories():
        lines = [f'{amount}, {category}' for amount, category in list_user_expenses_ordered_by_categories(user_data)]
        if not lines:
            print('no expenses')
        else:
            print('\n'.join(lines))

    @quit_on_eof
    def add_new_income():
        amount = read_amount_from_stdin('New income amount:')
        category = read_category_from_stdin('New income category:')
        date = read_date_from_stdin('New income date:')
        add_income(category, amount, date, user_data)

    @quit_on_eof
    def add_new_expense():
        amount = read_amount_from_stdin('New expense amount:')
        category = read_category_from_stdin('New expense category:')
        date = read_date_from_stdin('New expense date:')
        add_expense(category, amount, date, user_data)

    def exit_repl():
        nonlocal keep_going
        keep_going = False
    
    ops = {1: {'msg': 'show all data', 'handler': show_all_data},
           2: {'msg': 'show data for specific date', 'handler': show_data_for_specific_date},
           3: {'msg': 'show expenses, ordered by categories', 'handler': show_expenses_ordered_by_categories},
           4: {'msg': 'add new income', 'handler': add_new_income},
           5: {'msg': 'add new expense', 'handler': add_new_expense},
           6: {'msg': 'exit', 'handler': exit_repl}}

    option_lines = [f"{op} - {ops[op]['msg']}" for op in ops]
    option_text = 'Choose one of the following options to continue:\n{}'.format('\n'.join(option_lines))
    
    keep_going = True
    while keep_going:
        print(option_text)
        
        # at the end of the loop, op will be a valid option
        while True:
            try:
                op_str = input('>>> ')
                op = int(op_str)

                if 1 <= op <= len(ops):
                    break
                print(f'{op_str} is not a valid option.')
            except ValueError:
                print(f'could not interpret "{op_str}" as an option.')
                continue
        op_func = ops[op]['handler']
        op_func()
        print()
    
def main():
    if len(sys.argv) != 2:
        raise ValueError('expected 1 argument, but found {}'.format(len(sys.argv) - 1))
    filename = sys.argv[1]
    user_data = read_user_data_from_file(filename)
    repl(user_data)
    write_user_data_to_file(user_data, filename)
    
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
