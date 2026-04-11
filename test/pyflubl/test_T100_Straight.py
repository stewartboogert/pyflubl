import pyflubl as _pfbl
import numpy as _np
import os as _os

def make_T100_straight() :
    this_dir = _os.path.dirname(_os.path.abspath(__file__))

    m = _pfbl.BuilderNew.Machine(bakeTransforms=True)

    d = _pfbl.Fluka.Defaults('EM-CASCA')
    m.AddDefaults(d)

    b = _pfbl.Fluka.Beam(momentumOrKe=1, energySpread=0, sdum="ELECTRON")
    bp = _pfbl.Fluka.Beampos(xCentre=0, yCentre=0, zCentre=0, xCosine=0, yCosine=0)
    ba = _pfbl.Fluka.BeamAxes(xxCosine=1, xyCosine=0, xzCosine=0,
                              zxCosine=0, zyCosine=0, zzCosine=1)

    m.AddBeam(b)
    m.AddBeampos(bp)
    m.AddBeamaxes(ba)

    r = _pfbl.Fluka.Randomiz()
    m.AddRandomiz(r)

    s = _pfbl.Fluka.Start(10)
    m.AddStart(s)

    n = 5
    for i in range(0,n,1):
        m.AddDrift(name="d1_"+str(i), length=1,
                   beampipeMaterial="TUNGSTEN",
                   beampipeRadius=30, beampipeThickness=5)
        m.AddSamplerPlane(name="s1_"+str(i), length=1e-6)

    m.Write(this_dir+"/T100_Stright")

    return m

def test_T100_straight() :
    make_T100_straight()

if __name__ == "__main__":
    test_T100_straight()