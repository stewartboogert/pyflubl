import pyflubl as _pfbl
import pyg4ometry as _pyg4
import numpy as _np
import os as _os

def make_T035_Element_G4() :
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

    # custom geometry
    g4registry = m._GetGeant4Registry(True)
    outerMaterial = _pyg4.geant4.MaterialSingleElement("AIR",
                                                       atomic_number=1,
                                                       atomic_weight=1,
                                                       density=1)
    outersolid = _pyg4.geant4.solid.Tubs("custom_solid",0, 750, 1000, 0, _np.pi*2, g4registry)
    outerlogical = _pyg4.geant4.LogicalVolume(outersolid, outerMaterial, "custom_lv", g4registry)

    m.AddDrift(name="d1", length=1)
    m.AddSBend(name="b1", length=1, angle=_np.pi/6)
    m.AddDrift(name="d2", length=1)
    m.AddCustomG4(name="c1", length=1, containerLV = outerlogical, convertMaterials=False)
    m.AddSamplerPlane(name="s1", length=1e-6)
    m.Write(this_dir+"/T035_Element_G4")

    return m

def test_T035_Element_G4() :
    make_T035_Element_G4()

def make_T035_Element_G4_File() :
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

    m.AddDrift(name="d1", length=1)
    m.AddSBend(name="b1", length=1, angle=_np.pi/6)
    m.AddDrift(name="d2", length=1)
    m.AddCustomG4File(name="c1", length=1, geometryFile=this_dir+"/geometryInput/test_T035_Custom_Pyg4.gdml", lvName="bl")
    m.AddSamplerPlane(name="s1", length=1e-6)

    m.Write(this_dir+"/T035_Element_G4_File")

    return m

def test_T035_Element_G4_File() :
    make_T035_Element_G4_File()

def make_T035_Element_Fluka() :
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

    # custom fluka geometry
    reader = _pyg4.fluka.Reader(this_dir+"/geometryInput/test_T035_Custom_Fluka_Gap.inp")
    registry = reader.getRegistry()

    outer_bodies = [registry.bodyDict[k] for k in ['outer']]
    regions = [registry.regionDict[k] for k in ['OUTER','SHIELD','BEAM','TARGET']]

    m.AddDrift(name="d1", length=1)
    m.AddSBendSplit(name="b1", length=1, angle=_np.pi/8)
    m.AddDrift(name="d2", length=1)
    m.AddSamplerPlane(name="s1", length=1e-6)
    m.AddDrift(name="d3",length=1)
    m.AddSBendSplit(name="b2", length=2, angle=-_np.pi/8)
    m.AddDrift(name="d4", length=1)
    m.AddSamplerPlane(name="s2", length=1e-6)
    m.AddCustomFluka(name="c1",
                     length=1,
                     customOuterBodies = outer_bodies,
                     customRegions = regions,
                     flukaRegistry = registry)
    m.AddSamplerPlane(name="s3", length=1e-6)
    m.Write(this_dir+"/T035_Element_Fluka")

    return m

def test_T035_Element_Fluka() :
    make_T035_Element_Fluka()

def make_T035_Element_Fluka_File() :
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

    m.AddDrift(name="d1", length=1)
    m.AddSBendSplit(name="b1", length=1, angle=_np.pi/8)
    m.AddDrift(name="d2", length=1)
    m.AddSamplerPlane(name="s1", length=1e-6)
    m.AddDrift(name="d3",length=1)
    m.AddSBendSplit(name="b2", length=2, angle=-_np.pi/8)
    m.AddDrift(name="d4", length=1)
    m.AddSamplerPlane(name="s2", length=1e-6)
    m.AddCustomFlukaFile(name="c1", length=1,
                         geometryFile=this_dir+"/geometryInput/test_T035_Custom_Fluka_Gap.inp",
                         customOuterBodies= ['outer'],
                         customRegions=['OUTER','SHIELD','BEAM','TARGET'])
    m.AddSamplerPlane(name="s3", length=1e-6)

    m.Write(this_dir+"/T035_Element_Fluka_File")

    return m


def test_T035_Element_Fluka_File() :
    make_T035_Element_Fluka_File()


if __name__ == "__main__":
    test_T035_Element_G4()
    test_T035_Element_G4_File()
    test_T035_Element_Fluka()
    test_T035_Element_Fluka_File()