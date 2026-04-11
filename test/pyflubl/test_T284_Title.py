import pyflubl as _pfbl
import os as _os

def make_T284_title() :
    this_dir = _os.path.dirname(_os.path.abspath(__file__))

    m = _pfbl.BuilderNew.Machine(bakeTransforms=True)

    d = _pfbl.Fluka.Defaults('EM-CASCA')
    m.AddDefaults(d)

    t = _pfbl.Fluka.Title("TEST SIMULATION")
    m.AddTitle(t)

    b = _pfbl.Fluka.Beam(momentumOrKe=1, energySpread=0, sdum="ELECTRON")
    bp = _pfbl.Fluka.Beampos(xCentre=0, yCentre=0, zCentre=0, xCosine=0, yCosine=0)
    ba = _pfbl.Fluka.BeamAxes(xxCosine=1, xyCosine=0, xzCosine=0,
                              zxCosine=0, zyCosine=0, zzCosine=1)

    m.AddBeam(b)
    m.AddBeampos(bp)
    m.AddBeamaxes(ba)

    m.AddDrift(name="d1", length=1,
               beampipeMaterial = "TUNGSTEN",
               beampipeRadius=30, beampipeThickness=5)
    m.AddSamplerPlane(name="s1", length=1e-6)

    m.Write(this_dir+"/T284_Title")

    return m

def test_T050_title() :
    make_T284_title()

if __name__ == "__main__":
    test_T284_title()