import json as _json

def load_bookkeeping(bookkeeping_file):

    # open file
    f = open(bookkeeping_file,"r")

    # load JSON data
    d = _json.load(f)

    return d
