from pyg4ometry.fluka.card import Card as _Card

class Stepsize :

    def __init__(self, minStepSize = 10.0, maxStepSize = 1000, regionFrom = 0, regionTo = 0, regionStep = 1):
        self.minStepSize = minStepSize
        self.maxStepSize = maxStepSize
        self.regionFrom = regionFrom
        self.regionTo = regionTo
        self.regionStep = regionStep

        self.stepCard = _Card("STEPSIZE",
                              self.minStepSize, self.maxStepSize,
                              self.regionFrom, self.regionTo, self.regionStep)

    def AddRegistry(self, flukaregistry):
        if self.stepCard :
            flukaregistry.addCard(self.stepCard)

    def __repr__(self):
        retString = ""
        if self.stepCard :
            retString = self.stepCard.toFreeString()
        return retString