#-*-coding:utf-8-*-

def parse_file(fp, matrix_in=False):
    items = []
    if matrix_in:
        while True:
            first = fp.readline()
            if not first:
                break
            first = first.strip()
            for i in xrange(8):
                sys.stdin.readline()
            items.append(first)
    else:
        for line in fp:
            line = line.decode('utf-8').strip()
            item = line.split()[0]
            items.append(item)

    return items

