import itertools
import re

class Polynomial:
    # representation:
    # each item in self._dict represents a term.
    # the keys are the exponents and the values are the coefficients.
    # if an exponent is not in self._dict, the coefficient in the corresponding term is assumed to be 0
    
    # rep invariant: there will be no 0 coefficients.
    
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
        # assumes @d is a dictionary which maps nonnegative integers to ints
        # returns the corresponding Polynomial

        result = cls.__new__(cls)
        result._dict = {expt: coeff for expt, coeff in d.items() if coeff != 0}
        return result

    @classmethod
    def from_terms(cls, terms):
        # @terms must be an iterable of (expt, coeff) pairs
        # each expt must be a nonnegative int, and each coeff must be an int
        # if @terms is empty, the zero polynomial is returned
        result_dict = {}
        for expt, coeff in terms:
            result_dict[expt] = result_dict.get(expt, 0) + coeff
        result = cls.__new__(cls)
        result._dict = {expt: coeff for expt, coeff in result_dict.items() if coeff != 0}
        return result
    
    @classmethod
    def from_str(cls, poly_str):
        # converts the string @poly_str to a Polynomial
        # raises ValueError if the token sequence of @poly_str is not a <polynomial> (see below)
        # polynomial string grammar (the atomic elements of this grammar are tokens, not characters):
        # tokens:
        # <sign> := + | -
        # <int> := [0-9]+
        # <expt> := <int>
        # the grammar below is on tokens, not characters:
        # <unsigned-term> := <int> * x ^ <expt> | <int> * x | x ^ <expt> | x | <int>
        # <signed-term> := <sign> <unsigned-term>
        # <polynomial> := <sign>? <unsigned-term> <signed-term>*
        
        def parse_error(tokens, msg):
            raise ValueError(f'could not parse {tokens}: {msg}')

        def tokenize(poly_str):
            # a token is one of the following:
            # - a sequence of digits
            # - a sign: '+', '-', '*', '^'
            # - a variable: 'x'
            # possible performance improvement:
            # use indexes rather than creating new strings at each step

            result = []
            poly_str = ''.join(poly_str.split()) # remove whitespace
            while poly_str:
                first_char = poly_str[0]
                if first_char in '+-*^x':
                    result.append(first_char)
                    poly_str = poly_str[1:]
                elif first_char.isdigit():
                    digits = re.match(r'\d+', poly_str).group()
                    result.append(int(digits))
                    poly_str = poly_str[len(digits):]
                else:
                    raise ValueError(f'invalid character: {first_char}')
            return result
            
        def split_tokens(tokens):
            # @tokens must be an iterator and it must begin with a sign
            # splits @tokens into groups (lists) based on the signs '+' and '-'
            result = []
            current_group = [next(tokens)]
            for token in tokens:
                if token in ('+', '-'):
                    result.append(current_group)
                    current_group = [token]
                else:
                    current_group.append(token)
            result.append(current_group)
            return result
        
        def parse_token_group(token_group):
            # a token group has one of the following forms (where coeff and expt are nonnegative ints):
            #     - [<sign>, 'x']
            #     - [<sign>, coeff]
            #     - [<sign>, coeff, '*', 'x'],
            #     - [<sign>, 'x', '^', expt]
            #     - [<sign>, coeff, '*', 'x', '^', expt]
            # if @token_group does not have one of the above formats, a ValueError will be raised.
            # returns the (expt, coeff) pair corresponding to @token_group.
            # notice: no need to check that token_group[0] is a valid sign;
            #         this is guaranteed by the function split_tokens.
        
            # if len(token_group) < 6, add the extra parts yourself so that the len becomes 6
            if len(token_group) == 2:
                if token_group[1] == 'x':
                    # [<sign>, 'x']
                    token_group = [token_group[0], 1, '*', 'x', '^', 1]
                else:
                    # [<sign>, int]
                    token_group += ['*', 'x', '^', 0]
            elif len(token_group) == 4:
                if token_group[1] == 'x':
                    # [<sign>, 'x', '^', int]
                    token_group = [token_group[0], 1, '*', 'x', token_group[2], token_group[3]]
                else:
                    # [<sign>, int, '*', 'x']
                    token_group += ['^', 1]
            elif len(token_group) != 6:
                raise ValueError(f'unable to parse the token group {token_group}')
            
            # at this point len(token_group) == 6 is guaranteed
            
            sign, coeff, mul_sign, var, expt_sign, expt = token_group
            if type(coeff) is not int:
                raise ValueError(f'coefficient should be an int, but was given {coeff}')
            if mul_sign != '*':
                raise ValueError(f'invalid multiplication sign: {mul_sign}')
            if var != 'x':
                raise ValueError(f'invalid variable: {var}')
            if expt_sign != '^':
                raise ValueError(f'invalid exponentiation sign: {expt_sign}')
            if type(expt) is not int:
                raise ValueError(f'expt must be an int, but was given {expt}')
            return (expt, coeff if sign == '+' else -coeff)


        tokens = tokenize(poly_str)
        
        if not tokens:
            # poly_str contains only whitespace
            raise ValueError('cannot parse a whitespace string to a polynomial')
                
        if tokens[0] not in ('+', '-'):
            # for example when poly_str is "x^2 + 2*x + 1".
            # we want to infer a "+" before the first term.
            token_iter = itertools.chain(['+'], tokens)
        else:
            token_iter = iter(tokens)
        token_groups = split_tokens(token_iter)
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
        # for the term with exponent zero, 'x ^ 0' is not shown
        # for the term with exponent 1, '^ 1' is not shown
        # for terms with coefficient 1 or -1, the '1' is not shown
        
        if self.is_zero:
            return '0'

        def term_parts(term):
            expt, coeff = term
            result = []
            result.append('-' if coeff < 0 else '+')

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
        return Polynomial.from_terms((expt - 1, coeff * expt)
                                     for expt, coeff in self.terms
                                     if expt != 0)
        
