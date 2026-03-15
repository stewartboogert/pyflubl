import pyflubl as _pfbl
import os as _os

def make_T027_wirescanner() :
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

    s = _pfbl.Fluka.Start(1000)
    m.AddStart(s)

    m.AddDrift(name="d1", length=1)
    m.AddSamplerPlane(name="s1", length=1e-6)

    m.AddWireScanner(name="ws1", length=0.1,
                     wireAngle=0.0,
                     wireLength=30,
                     wireDiameter=2.5)
    m.AddSamplerPlane(name="s2", length=1e-6)

    m.AddDrift(name="d3", length=1)
    m.AddSamplerPlane(name="s3", length=1e-6)

    m.Write(this_dir+"/T027_Wirescanner")

    return m

def test_T027_wirescanner() :
    make_T027_wirescanner()

if __name__ == "__main__":
    test_T027_wirescanner()