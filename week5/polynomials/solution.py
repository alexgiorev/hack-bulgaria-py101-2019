import sys
from polynomial import Polynomial

if len(sys.argv) == 1:
    print("expected an argument, but didn't find it")
    exit()
elif len(sys.argv) != 2:
    print(f"expected a single argument, but found {len(sys.argv)}")
    exit()

poly_str = sys.argv[1]
    
try:
    poly = Polynomial.parse(sys.argv[1])
except ValueError:
    print(f'could not parse "{poly_str}" to a polynomial')

print(poly.derivative)
