import unittest
from polynomial import Polynomial

class TestPolynomial(unittest.TestCase):
    def test_from_str_constructor(self):
        # empty string raises ValueError
        self.assertRaises(ValueError, Polynomial.from_str, '')
        
        # multiplication sign is required
        self.assertRaises(ValueError, Polynomial.from_str, '2 x')
        
        # x is the only allowed variable
        self.assertRaises(ValueError, Polynomial.from_str, 'y ^ 2')
        
        # the exponentiation sign is ^
        self.assertRaises(ValueError, Polynomial.from_str, 'x**2')
        
        # you can have arbitrary whitespace between tokens
        self.assertEqual(Polynomial.from_str('x    ^ 2 + 3*x^3-4'),
                         Polynomial.from_dict({3: 3, 2:1, 0:-4}))
        
        # terms with the same exponents are automatically added
        self.assertEqual(Polynomial.from_str('x^2 + 2*x^2 + 3*x^2'),
                         Polynomial.from_str('6*x^2'))
        self.assertTrue(Polynomial.from_str('x^3 - x^3').is_zero)
        
        # this example shows all 5 possible forms of terms
        self.assertEqual(Polynomial.from_str('-3*x^10 + 7*x + x^5 - x + 5'),
                         Polynomial.from_dict({10: -3, 1: 6, 5: 1, 0: 5}))

    def test_from_dict_constructor(self):
        # you can have zero coefficients
        self.assertEqual(Polynomial.from_dict({3: 0, 2: 1, 1: 2, 0: 1}),
                         Polynomial.from_str('x^2 + 2*x + 1'))
        
        # the empty dict results in the zero Polynomial
        self.assertEqual(Polynomial.from_dict({}), Polynomial.zero())

        # only zero coefficients result in the zero Polynomial
        self.assertTrue(Polynomial.from_dict({4: 0, 3: 0, 1: 0}).is_zero)

    def test_from_terms_constructor(self):
        # you can have the same exponent many times, the coeffs are automatically accumulated
        self.assertEqual(Polynomial.from_terms([(3, 4), (2, -2), (2, 3), (0, 1)]),
                         Polynomial.from_str('4*x^3 + x^2 + 1'))
        self.assertTrue(Polynomial.from_terms({(3, 4), (3, -4)}).is_zero)

        # any empty iterable results in the zero polynomial
        self.assertTrue(Polynomial.from_terms(set()).is_zero)

    def test_str(self):
        # tokens are separated by single blank
        self.assertEqual(str(Polynomial.from_str('-3*x^2')), '- 3 * x ^ 2')

        # terms are sorted by exponents
        self.assertEqual(str(Polynomial.from_str('1 + x + x^2')), 'x ^ 2 + x + 1')
        
        # for the term with exponent zero, 'x ^ 0' is not shown
        self.assertEqual(str(Polynomial.from_str('x^2 + 3*x^0')), 'x ^ 2 + 3')

        # for the term with exponent 1, '^ 1' is not shown
        self.assertEqual(str(Polynomial.from_str('x^2 + 2*x^1')), 'x ^ 2 + 2 * x')

        # for the term with coefficient 1 or -1, the '1' is not shown
        self.assertEqual(str(Polynomial.from_str('x^2 + 1*x^3')), 'x ^ 3 + x ^ 2')
        self.assertEqual(str(Polynomial.from_str('x^2 - 1*x^3')), '- x ^ 3 + x ^ 2')
        

unittest.main()
