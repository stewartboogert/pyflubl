import pyflubl as _pfbl
import numpy as _np
import os as _os

def make_quad(tilt = 0, offsetX = 0, offsetY = 0, fileName = "T006_Quad"):
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

    uic = _pfbl.Fluka.Usricall()
    m.AddUsricall(uic)

    ud = _pfbl.Fluka.Userdump(mgdraw=100,lun=23,mgdrawOption=-1,userDump=None, outputFile="dump")
    m.AddUserdump(ud)

    uoc = _pfbl.Fluka.Usrocall()
    m.AddUsrocall(uoc)

    m.AddDrift(name="d1", length=1)
    m.AddSamplerPlane(name="s1", length=1e-6)
    m.AddQuadrupole(name="q1", length=0.5, k1=0.5, tilt=tilt, offsetX=offsetX, offsetY=offsetY)
    m.AddSamplerPlane(name="s2", length=1e-6)
    m.AddDrift(name="d2", length=1)

    m.Write(this_dir+"/"+fileName)

    return m

def test_T004_quad() :
    make_quad(fileName="T004_Quad")

def test_T004_quad_tilt() :
    make_quad(tilt=_np.pi/4, fileName="T004_Quad_tilt")

def test_T004_quad_offsetX() :
    make_quad(offsetX=1, fileName="T004_Quad_offsetX")

def test_T004_quad_offsetY() :
    make_quad(offsetY=1, fileName="T004_Quad_offsetY")

if __name__ == "__main__":
    test_T004_quad()