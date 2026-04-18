import pyflubl as _pfbl
import numpy as _np
import os as _os

def make_T051_Lattice_Drift() :
    this_dir = _os.path.dirname(_os.path.abspath(__file__))

    m = _pfbl.BuilderNew.Machine(bakeTransforms=True)

    d = _pfbl.Fluka.Defaults('EM-CASCA')
    m.AddDefaults(d)

    b = _pfbl.Fluka.Beam(momentumOrKe=1, energySpread=0.0, sdum="ELECTRON")
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

    uic = _pfbl.Fluka.Usricall()
    m.AddUsricall(uic)

    uoc = _pfbl.Fluka.Usrocall()
    m.AddUsrocall(uoc)

    ud = _pfbl.Fluka.Userdump(mgdraw=100,lun=23,mgdrawOption=-1,userDump=None, outputFile="dump")
    m.AddUserdump(ud)

    # set world material
    m.world_material = "VACUUM"

    m.AddDrift(name="d1",
               length=1,
               beampipeMaterial = "IRON",
               outerMaterial = "AIR")

    d2 = m.AddDrift("d2",
                   length=0.2,
                   beampipeMaterial="IRON",
                   outerMaterial="AIR",
                   add=False)

    d3 = m.AddDrift("d3",
                   length=0.4,
                   beampipeMaterial="IRON",
                   outerMaterial="AIR",
                   add=False)

    m.AddLatticePrototype(d2)
    m.AddLatticePrototype(d3)

    m.AddLatticeInstance("d2i1","d2")
    m.AddLatticeInstance("d3i1","d3")

    m.AddLatticeInstance("d2i2","d2")
    m.AddLatticeInstance("d3i2","d3")

    m.AddLatticeInstance("d2i3","d2")
    m.AddLatticeInstance("d3i3","d3")

    m.AddLatticeInstance("d2i4","d2")
    m.AddLatticeInstance("d3i4","d3")

    m.Write(this_dir+"/T051_Lattice_Drift")

    return m

def test_T051_Lattice_Drift() :
    make_T051_Lattice_Drift()

def make_T051_Lattice_RBend() :
    this_dir = _os.path.dirname(_os.path.abspath(__file__))

    m = _pfbl.BuilderNew.Machine(bakeTransforms=True)

    d = _pfbl.Fluka.Defaults('EM-CASCA')
    m.AddDefaults(d)

    b = _pfbl.Fluka.Beam(momentumOrKe=1, energySpread=0.0, sdum="ELECTRON")
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

    uic = _pfbl.Fluka.Usricall()
    m.AddUsricall(uic)

    uoc = _pfbl.Fluka.Usrocall()
    m.AddUsrocall(uoc)

    ud = _pfbl.Fluka.Userdump(mgdraw=100,lun=23,mgdrawOption=-1,userDump=None, outputFile="dump")
    m.AddUserdump(ud)

    # set world material
    m.world_material = "VACUUM"

    d1 = m.AddDrift(name="d1",
                    length=0.25,
                    beampipeMaterial = "IRON",
                    outerMaterial = "AIR",
                    add=False)

    rb1 = m.AddRBend(name="rb1",
                     length=0.25,
                     angle=_np.pi*5/180.0,
                     add=False)

    m.AddLatticePrototype(d1)
    m.AddLatticePrototype(rb1)

    m.AddLatticeInstance("d1i1","d1")
    m.AddLatticeInstance("rb1i1","rb1")

    m.Write(this_dir+"/T051_Lattice_RBend")

    return m

def test_T051_Lattice_RBend() :
    make_T051_Lattice_RBend()

def make_T051_Lattice_SBend() :
    this_dir = _os.path.dirname(_os.path.abspath(__file__))

    m = _pfbl.BuilderNew.Machine(bakeTransforms=True)

    d = _pfbl.Fluka.Defaults('EM-CASCA')
    m.AddDefaults(d)

    b = _pfbl.Fluka.Beam(momentumOrKe=1, energySpread=0.0, sdum="ELECTRON")
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

    uic = _pfbl.Fluka.Usricall()
    m.AddUsricall(uic)

    uoc = _pfbl.Fluka.Usrocall()
    m.AddUsrocall(uoc)

    ud = _pfbl.Fluka.Userdump(mgdraw=100,lun=23,mgdrawOption=-1,userDump=None, outputFile="dump")
    m.AddUserdump(ud)

    # set world material
    m.world_material = "VACUUM"

    d1 = m.AddDrift(name="d1",
                    length=0.25,
                    beampipeMaterial = "IRON",
                    outerMaterial = "AIR",
                    add=False)

    sb1 = m.AddSBend(name="sb1",
                     length=0.25,
                     angle=_np.pi*5/180.0,
                     add=False)

    sb2 = m.AddSBend(name="sb2",
                     length=0.25,
                     angle=-_np.pi*5/180.0,
                     add=False)

    m.AddLatticePrototype(d1)
    m.AddLatticePrototype(sb1)
    m.AddLatticePrototype(sb2)

    m.AddLatticeInstance("d1i1","d1")
    m.AddLatticeInstance("sb1i1","sb1")

    m.AddLatticeInstance("d1i2","d1")
    m.AddLatticeInstance("sb1i2","sb1")

    m.AddLatticeInstance("d1i3","d1")
    m.AddLatticeInstance("sb1i3","sb1")

    m.AddLatticeInstance("d1i4","d1")
    m.AddLatticeInstance("sb1i4","sb1")

    m.AddLatticeInstance("d1i5","d1")
    m.AddLatticeInstance("sb1i5","sb1")

    m.AddLatticeInstance("d1i6","d1")
    m.AddLatticeInstance("sb2i1","sb2")

    m.AddLatticeInstance("d1i7","d1")
    m.AddLatticeInstance("sb2i2","sb2")

    m.AddLatticeInstance("d1i8","d1")
    m.AddLatticeInstance("sb2i3","sb2")

    m.AddLatticeInstance("d1i9","d1")
    m.AddLatticeInstance("sb2i4","sb2")

    m.AddLatticeInstance("d1i10","d1")
    m.AddLatticeInstance("sb2i5","sb2")

    m.AddSamplerPlane(name="s1", length=1e-4)

    m.Write(this_dir+"/T051_Lattice_SBend")

    return m

def test_T051_Lattice_SBend() :
    make_T051_Lattice_SBend()