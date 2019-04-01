def reduce_file_path(path):
    parts = path.split('/')
    current_path = []
    for part in parts:
        if not part or part == '.':
            continue
        elif part == '..':
            if current_path:
                current_path.pop()
        else:
            current_path.append(part)
    return '/' + '/'.join(current_path)
        
def test_reduce_file_path():
    rfp = reduce_file_path
    assert (rfp('/home//rositsazz/courses/./Programming-101-Python-2019/week02/../') ==
            '/home/rositsazz/courses/Programming-101-Python-2019')
    assert rfp('/') == '/'
    assert rfp("/srv/www/htdocs/wtf/") == "/srv/www/htdocs/wtf"
    assert rfp("/srv/./././././") == "/srv"
    assert rfp("/etc//wtf/") == "/etc/wtf"
    assert rfp("/etc/../etc/../etc/../") == "/"
    assert rfp("//////////////") == "/"
    assert rfp("/../") == "/"
    
test_reduce_file_path()
