import sys

def path_chapters(path):
    # returns an iterator of chapters from the file referenced by @path
    # @path's first line must start with #
    
    with open(path) as f:
        lines = list(f)

    current_chapter = [lines[0]]
    for line in itertools.islice(lines, 1, len(lines)):
        if line[0] == '#':
            yield current_chapter
            current_chapter = [line]
        else:
            current_chapter.append(line)
    yield current_chapter

def path_chapters2(path):
    # returns an iterator of chapters from the file referenced by @path
    # @path's first line must start with #
    # the difference with path_chapters is that this does not read the
    # whole file at once

    with open(path) as f:    
        current_chapter = [next(f)]
        for line in f:
            if line[0] == '#':
                yield current_chapter
                current_chapter = [line]
            else:
                current_chapter.append(line)
        yield current_chapter

def getChar():
    # got this from here: https://stackoverflow.com/a/36974338/4180854
    # for POSIX-based systems (with termios & tty support)
    
    import tty, sys, termios

    fd = sys.stdin.fileno()
    oldSettings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        answer = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

    return answer
        
for path in sys.argv[1:]:
    for chap in path_chapters2(path):
        print(''.join(chap), end='')
        while True:
            c = getChar()
            if c == ' ':
                break
            elif c == 'q':
                exit()
    print()
