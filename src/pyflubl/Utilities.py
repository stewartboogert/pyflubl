import json as _json

def load_bookkeeping(bookkeeping_file):

    # open file
    with open(bookkeeping_file, "r", encoding="utf-8") as f:

        # load JSON data
        d = _json.load(f)

        return d
