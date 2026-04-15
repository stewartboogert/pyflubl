from pyg4ometry.fluka.card import Card as _Card
from ._BaseCard import BaseCard as _BaseCard

class Lattice(_BaseCard):

    def __init__(self,
                 prototypeBody=None,
                 instanceRegion=None,
                 rotDefiName=None):
        super().__init__()
        self.prototypeBody = prototypeBody
        self.instanceRegion = instanceRegion

        self.card = _Card("LATTICE", instanceRegion, None, None, prototypeBody, None, None, rotDefiName)

    def AddRegistry(self, flukaregistry):
        flukaregistry.addLatticeCard(self.card)