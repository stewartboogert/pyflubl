from pyg4ometry.fluka.card import Card as _Card
from ._BaseCard import BaseCard as _BaseCard

class Plotgeom(_BaseCard):

    def __init__(self,
                 plotAxes = 0,
                 plotRegions = 0,
                 plotRegionNumbering = 0,
                 wormLength=None,
                 diagnosticPrint=None,
                 plotLUN=40,
                 sdum="FORMAT"):
        super().__init__()

        self.card = _Card("PLOTGEOM", plotAxes, plotRegions, plotRegionNumbering,
                          wormLength, diagnosticPrint, plotLUN, sdum)