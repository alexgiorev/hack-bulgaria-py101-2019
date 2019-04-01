import math
import functools

def verify_fraction(x):
    if type(x) is not tuple:
        raise TypeError(f'expected a tuple, but was given a {type(x)}')
    
    if len(x) != 2:
        raise ValueError(f'fraction should have length 2, but has length {len(x)}')
    
    num, denom = x
    
    if type(num) is not int:
        raise TypeError(f'numerator should be an int. was given a {type(num)}')
    
    if type(denom) is not int:
        raise TypeError(f'denominator should be an int. was given a {type(denom)}')

    if denom == 0:
        raise ZeroDivisionError(f'denominator cannot be 0. given {x}')

def simplify_fraction(fraction):
    verify_fraction(fraction)
    return simplify_fraction_partial(fraction)

def simplify_fraction_partial(fraction):
    # assumes fraction is a valid fraction
    
    num, denom = fraction
    gcd = math.gcd(num, denom)
    sig = -1 if num * denom < 0 else 1
    return (sig * abs(num // gcd), abs(denom // gcd))

def add_fractions(frac1, frac2):
    # if @frac1 or @frac2 is not a valid fraction,
    # an appropriate exception will be raised
    # returns the simplified sum of @frac1 and @frac2
    
    verify_fraction(frac1)
    verify_fraction(frac2)
    return add_fractions_partial(frac1, frac2)

def add_fractions_partial(frac1, frac2):
    # assumes @frac1 and @frac2 are valid fractions
    # returns the simplified sum of @frac1 and @frac2
    n1, d1 = frac1
    n2, d2 = frac2
    return simplify_fraction_partial((n1 * d2 + n2 * d1, d1 * d2))

def verify_fractions(fractions):
    # raises an appropriate exception when one of the fractions in
    # @fractions is not valid
    
    for fraction in fractions:
        verify_fraction(fraction)

def collect_fractions(fractions):
    # if any of the fractions in @fractions is not valid,
    # an appropriate exception will be raised
    # returns the sum of the @fractions
    
    validate_fractions(fractions)
    return functools.reduce(add_fractions_partial, fractions)

def cmp_fracs(frac1, frac2):
    # assumes frac1 and frac2 are valid fractions
    # returns -1 if frac1 < frac2, 0 if frac1 == frac2 and 1 if frac1 > frac2
    
    simplified_frac1, simplified_frac2 = simplify_fraction(frac1), simplify_fraction(frac2)
    num1, denom1 = simplified_frac1
    num2, denom2 = simplified_frac2

    if simplified_frac1 == simplified_frac2:
        return 0
    
    if num1 * num2 >= 0:
        return -1 if num1 * denom2 < num2 * denom1 else 1

    return -1 if num1 < 0 else 1

def sort_fractions(lof):
    # if any of the values in @lof is not a valid fraction,
    # an appropriate exception will be raised
    # returns a new list that has the same values as @lof,
    # but is sorted in ascending order
    
    verify_fractions(lof)
    return sorted(lof, key=functools.cmp_to_key(cmp_fracs))

