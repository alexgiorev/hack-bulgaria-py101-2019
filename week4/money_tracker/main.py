import sys
import parse
import constants

def repl(user_data):
    def quit_on_eof(handler):
        # for options which, when the user presses crtl-d
        # we go back to the main menu
        
        def result():
            try:
                handler()
            except EOFError:
                pass
        return result

    def show_all_data():
        print(parse.db_to_str(user_data))
    
    @quit_on_eof
    def show_data_for_specific_date():
        # after this loop, the variable date will be a valid date
        # restict to amount, category, type
        # the tuple must satisfy that we have a given date
        # the prefinal result is not sorted

        print('enter date:')
        date = parse.read_date_from_stdin()
        is_from_date = user_data.make_query_condition(lambda current_date: current_date == date, column_names={'date'})
        print('\n'.join(f'{amount}, {category}, {_type}' for amount, category, _type in
                        user_data.query(is_from_date, restrict_to={'amount', 'category', 'type'})))

    def show_expenses_ordered_by_categories():
        # restrict to amount and category
        # the tuple must be an expense
        # sort the result based on the category

        is_expense = user_data.make_query_condition(lambda _type: _type == constants.EXPENSE_STR, column_names={'type'})
        print('\n'.join(f'{amount}, {category}' for amount, category in
                        user_data.query(is_expense, restrict_to={'amount', 'category'}, sort_by={'category'})))
              
    @quit_on_eof
    def add_new_income():
        print('enter date:')
        date = parse.read_date_from_stdin()
        print('enter amount:')
        amount = parse.read_amount_from_stdin()
        print('enter category:')
        category = parse.read_category_from_stdin()
        user_data.add_tuple(date, amount, category, constants.INCOME_STR)

    @quit_on_eof
    def add_new_expense():
        print('enter date:')
        date = parse.read_date_from_stdin()
        print('enter amount:')
        amount = parse.read_amount_from_stdin()
        print('enter category:')
        category = parse.read_category_from_stdin()
        user_data.add_tuple(date, amount, category, constants.EXPENSE_STR)

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
        raise ValueError(f'expected 1 argument, but found {len(sys.argv) - 1}')
    filename = sys.argv[1]
    user_data = parse.read_database_from_file(filename)
    repl(user_data)
    parse.write_database_to_file(user_data, filename)
    
if __name__ == '__main__':
    main()
