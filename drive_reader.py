import sys
sys.path.append("../pypy")

def target(driver, args):
    driver.exe_name = '__last__test'
    from clojure_metal.lang.lisp_reader import read_string

    def entry_point(argv):
        v = read_string(argv[1])
        return 0

    return entry_point, None

class Dummy():
    pass

import sys
if __name__ == '__main__':
    entry, _ = target(Dummy, [])
    entry(sys.argv)