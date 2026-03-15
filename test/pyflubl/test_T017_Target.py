import pyflubl as _pfbl
import os as _os

def make_T017_target_circular() :
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
    m.AddTarget(name="t1", length=1,
                horizontalWidth=200,
                verticalWidth=200,
                apertureType="circular",
                material="IRON",
                outerMaterial="AIR")
    m.AddSamplerPlane(name="s1", length=1e-6)
    m.AddDrift(name="d2", length=1)
    m.AddTarget(name="t2", length=1,
                horizontalWidth=200,
                verticalWidth=200,
                apertureType="circular",
                material="IRON",
                outerMaterial="AIR")
    m.AddSamplerPlane(name="s2", length=1e-6)

    m.Write(this_dir+"/T017_target_circular")

    return m

def test_T017_target_circular() :
    make_T017_target_circular()

def make_T017_target_elliptical() :
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
    m.AddTarget(name="t1", length=1,
                horizontalWidth=250,
                verticalWidth=150,
                apertureType="elliptical",
                material="IRON",
                outerMaterial="AIR")
    m.AddSamplerPlane(name="s1", length=1e-6)
    m.AddDrift(name="d2", length=1)
    m.AddTarget(name="t2", length=1,
                horizontalWidth=150,
                verticalWidth=250,
                apertureType="elliptical",
                material="IRON",
                outerMaterial="AIR")
    m.AddSamplerPlane(name="s2", length=1e-6)

    m.Write(this_dir+"/T017_target_elliptical")

    return m

def test_T017_target_elliptical() :
    make_T017_target_elliptical()

def make_T017_target_rectangular() :
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
    m.AddTarget(name="t1", length=1,
                horizontalWidth=250,
                verticalWidth=150,
                apertureType="rectangular",
                material="IRON",
                outerMaterial="AIR")
    m.AddSamplerPlane(name="s1", length=1e-6)
    m.AddDrift(name="d2", length=1)
    m.AddTarget(name="t2", length=1,
                horizontalWidth=150,
                verticalWidth=250,
                apertureType="rectangular",
                material="IRON",
                outerMaterial="AIR")
    m.AddSamplerPlane(name="s2", length=1e-6)

    m.Write(this_dir+"/T017_target_rectangular")

    return m

def test_T017_target_rectangular() :
    make_T017_target_rectangular()

if __name__ == "__main__":
    test_T017_target_circular()
    test_T017_target_elliptical()