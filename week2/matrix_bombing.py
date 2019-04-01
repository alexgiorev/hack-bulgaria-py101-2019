import copy

def matrix_sum(m):
    return sum(map(sum, m))

def get_neighbours(bri, bci, nrows, ncols):
    # returns an iterator which yields all neighbours of (bri, bci)
    # for a matrix with @nrows rows and @ncols columns
    def is_good(coords):
        r, c = coords
        return 0 <= r < nrows and 0 <= c < ncols

    suggestion = ((bri-1, bci-1), (bri-1, bci), (bri-1, bci+1),
                  (bri, bci-1), (bri, bci+1),
                  (bri+1, bci-1), (bri+1, bci), (bri+1, bci+1))
    
    return filter(is_good, suggestion)

def bomb(m, bri, bci):
    # returns a new matrix that is the result of
    # bombing m at the coordinates (ri, ci)
    out = copy.deepcopy(m)
    nrows = len(m)
    ncols = len(m[0])
    val = m[bri][bci]
    for ri, ci in get_neighbours(bri, bci, nrows, ncols):
        nval = out[ri][ci]
        out[ri][ci] = max(0, nval - val)
    return out
    
def matrix_bombing_plan(m):
    result = {}
    nrows = len(m)
    ncols = len(m[0])
    for ri in range(nrows):
        for ci in range(ncols):
            bombed = bomb(m, ri, ci)
            result[ri, ci] = matrix_sum(bombed)
    return result

m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for k, v in matrix_bombing_plan(m).items():
    print(k, v)
