import time
import datetime

class performance:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.start = time.time()

    def write_time_taken(self):
        time_taken = self.end - self.start
        with open(self.filename, 'a') as f:
            f.write(f'{datetime.datetime.now()}. Execution time: {time_taken}\n')
    
    def __exit__(self, exc_type, exc, trace):
        self.end = time.time()
        self.write_time_taken()
        
if __name__ == '__main__':        
    def perftest(n):
        for k in range(n):
            pass

    # test
    with performance('perflog'):
        n = 100000000
        for k in range(n):
            pass
        print('ending the block')
