import itertools

class Polynomial:
    # ==================================================
    # data abstraction functions
    # make sure all procedures after the data abstraction block use the
    # procedures inside the data abstraction block

    @classmethod
    def zero(cls):
        # returns the zero polynomial
        result = cls.__new__(cls)
        result._dict = {}
        return result
    
    @classmethod
    def from_dict(cls, d):
        # accepts a dict which maps exponents to coefficients
        # assumes @d is a dictionary which maps nonnegative integers to ints
        # returns the corresponding Polynomial

        result = cls.__new__(cls)
        result._dict = {expt: coeff for expt, coeff in d.items() if coeff != 0}
        return result

    @classmethod
    def from_terms(cls, terms):
        # @term must be an iterable of (expt, coeff) pairs where each expt is nonnegative
        result_dict = {}
        for expt, coeff in terms:
            result_dict[expt] = result_dict.get(expt, 0) + coeff
        result = cls.__new__(cls)
        result._dict = {expt: coeff for expt, coeff in result_dict.items() if coeff != 0}
        return result
    
    @classmethod
    def from_str(cls, poly_str):
        # converts the string @poly_str to a Polynomial
        # raises ValueError if poly_str.split() is not a <polynomial> (see below)
        # polynomial string grammar: 
        # <term> := <int> * x ^ <expt> | <int> * x | x ^ <expt> | x | <int>
        # <expt> := nonnegative int
        # <signed-term> := (+|-) <term>
        # <polynomial> := <term> <signed-term>*

        def parse_error(tokens, msg):
            raise ValueError(f'could not parse {tokens}: {msg}')

        # it will maybe be better if you read split_tokens and parse_token_group
        # after first reading the code after them
        
        def split_tokens(tokens):
            # splits @tokens into groups (lists) based on the signs '+' and '-'
            result = []
            current_group = ['+']
            for token in tokens:
                if token in ('+', '-'):
                    result.append(current_group)
                    current_group = [token]
                else:
                    current_group.append(token)
            result.append(current_group)
            return result

        def parse_token_group(token_group):
            # a token group has one of the following forms:
            #     - [<sign>, 'x']
            #     - [<sign>, <int>]
            #     - [<sign>, <int>, '*', 'x'],
            #     - [<sign>, 'x', '^', <expt>]
            #     - [<sign>, <int>, '*', 'x', '^', <expt>]
            # if @token_group does not have one of the above formats, a ValueError will be raised
            # returns the (expt, coeff) pair corresponding to @token_group
            # NOTICE: no need to check that token_group[0] is a valid sign;
            #         this is guaranteed by the function split_tokens

            # if len(token_group) != 6, add the extra parts yourself so that the len becomes 6
            if len(token_group) == 2:
                if token_group[1] == 'x':
                    # [<sign>, 'x']
                    token_group = [token_group[0], '1', '*', 'x', '^', '1']
                else:
                    # [<sign>, <int>]
                    coeff_str = token_group[1]
                    token_group = [token_group[0], coeff_str, '*', 'x', '^', '0']
            elif len(token_group) == 4:
                if token_group[1] == 'x':
                    # [<sign>, 'x', '^', <expt>]
                    expt_sign, expt_str = token_group[2], token_group[3]
                    token_group = [token_group[0], '1', '*', 'x', expt_sign, expt_str]
                else:
                    # [<sign>, <int>, '*', 'x']
                    coeff_str, mul_sign, var = token_group[1:]
                    token_group = [token_group[0], coeff_str, mul_sign, var, '^', '1']
            elif len(token_group) != 6:
                raise ValueError(f'unable to parse the token group {token_group}')
            
            # at this point len(token_group) == 6 is guaranteed
            
            sign, coeff_str, mul_sign, var, expt_sign, expt_str = token_group
            coeff = int(coeff_str) # will raise ValueError if @int_str cannot be parsed to an int
            if mul_sign != '*':
                raise ValueError(f'invalid multiplication sign: {mul_sign}')
            if var != 'x':
                raise ValueError(f'invalid variable: {var}')
            if expt_sign != '^':
                raise ValueError(f'invalid exponentiation sign: {expt_sign}')
            expt = int(expt_str) # will raise ValueError if expt_str cannot be parsed to an int                
            if expt < 0:
                raise ValueError(f'expt must be nonnegative, but was given {expt}')
            return (expt, coeff if sign == '+' else -coeff)
    
        tokens = poly_str.split()
        token_groups = split_tokens(tokens)
        return cls.from_terms(map(parse_token_group, token_groups))        

    @property
    def terms(self):
        # returns an iterator of (expt, coeff) pairs representing @self's non-zero terms.
        # the order is not specified.
        return self._dict.items()

    @property
    def is_zero(self):
        return not self._dict

    def coeff_at(self, expt):
        # returns the coefficient of the term with exponent @expt
        # if expt is not an integer, a TypeError is raised
        # if expt is negative, a ValueError is raised

        if type(expt) is not int:
            raise TypeError(f'expt should be a nonnegative integer; given: {type(expt)}')

        if expt < 0:
            raise ValueError(f'expt should be a nonnegative integer; given: {expt}')

        return self._dict.get(expt, 0)

    def __str__(self):
        # TODO: document
        
        if self.is_zero:
            return '0'

        def term_parts(term):
            expt, coeff = term
            result = []
            result.append('-' if coeff < 0 else '+') # append sign

            if abs(coeff) == 1:
                if expt == 0:
                    result.append('1')
                elif expt == 1:
                    result.append('x')
                else:
                    result.extend(['x', '^', str(expt)])
            else:
                result.append(str(abs(coeff)))
                if expt == 1:
                    result.extend(['*', 'x'])
                elif expt > 1:
                    result.extend(['*', 'x', '^', str(expt)])
                    
            return result

        terms = sorted(self.terms, reverse=True)
        first_term = terms[0]
        first_parts = term_parts(first_term)
        if first_parts[0] == '+':
            first_parts = first_parts[1:]
        else:
            first_parts = ['-' + first_parts[1]] + first_parts[2:]
        rest_parts = itertools.chain.from_iterable(map(term_parts, terms[1:]))
        all_parts = itertools.chain(first_parts, rest_parts)
        return ' '.join(all_parts)

    
    # end data abstraction functions block
    # ==================================================
    
    @property
    def derivative(self):
        # returns the polynomial that is the derivative of @self
        
        if self.is_zero:
            return Polynomial.zero()
        
        result_dict = {}
        
        for expt, coeff in self.terms:
            if expt != 0:
                result_dict[expt-1] = coeff * expt

        return Polynomial.from_dict(result_dict)
