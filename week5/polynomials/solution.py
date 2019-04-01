import sys
from polynomial import Polynomial

if len(sys.argv) != 2:
    print(f"expected a single argument, but found {len(sys.argv) - 1}")
    exit()

poly_str = sys.argv[1]
    
try:
    poly = Polynomial.from_str(sys.argv[1])
except ValueError as parse_error:
    print(f'could not parse "{poly_str}" to a polynomial: {parse_error}')
else:
    print(poly.derivative)
