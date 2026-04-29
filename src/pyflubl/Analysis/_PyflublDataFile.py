try :
    import ROOT as _ROOT
except ImportError :
    print("ROOT not found")

try :
    import uproot as _uproot
except ImportError :
    print("uproot not found")

import numpy as _np

from ..Coordinates import Coordinates as _Coordinates
from ._open import openFile as _openFile
from ._plot import plot_coordinates_projection as _plot_coordinates_projection
from ._plot import plot_usrdump as _plot_usrdump

class PyflublOutput:

    def __init__(self,
                 jsonFileName = None,
                 jsonCoordinateFileName = None,
                 dumpFileName = None,
                 rootFileName = None,
                 usrbinFileName = None,
                 usrbnxFileName = None):

        if jsonFileName is not None:
            self.bookkeeping = load_bookkeeping(jsonFileName)
        if jsonCoordinateFileName is not None:
            self.coordinates = load_coorinates(jsonCoordinateFileName)
        if dumpFileName is not None:
            self.dumpFile = _openFile(dumpFileName,"usrdump")
        if rootFileName is not None:
            uprootFile = _uproot.open(rootFileName)
            self.uprootTree = uprootFile["event"]
            # self.rootPandas = uprootTree.array(library="pd")
        if usrbinFileName is not None:
            self.usrbinFile = _openFile(usrbinFileName,"usrbin")

    def plot_projection(self,
                        projection = "zx",
                        eventNumber = 0,
                        detector = -1):
        if self.coordinates is not None:
            _plot_coordinates_projection(self.coordinates, projection=projection,
                                         plotCoordinateMarkers=False,
                                         plotNormals=False,
                                         plotFilledElements=False)
        if self.dumpFile is not None:
            self.dumpFile.read_event(eventNumber)
            _plot_usrdump(self.dumpFile,projection=projection)

        if self.usrbinFile is not None:
            pass

def load_bookkeeping(file_name) :
    import json
    with open(file_name, "r") as f :
        bookkeeping = json.load(f)
    return bookkeeping

def load_coorinates(file_name):
    c = _Coordinates()
    c.LoadJSON(file_name)
    return c