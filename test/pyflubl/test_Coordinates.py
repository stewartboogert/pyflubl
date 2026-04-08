import pyflubl as _pfbl
import numpy as _np
import os as _os

def test_T001_Drift_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e = m.AddDrift("d1", length=1)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T001_Drift_coordinates.json")

    # return c

def test_T001_Drift_many_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e1 = m.AddDrift("d1", length=1)
    e2 = m.AddDrift("d2", length=2)
    e3 = m.AddDrift("d3", length=3)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e1)
    c.Append(e2)
    c.Append(e3)

    c.Build()
    c.SaveJSON("T001_Drift_many_coordinates.json")

    # return c

def test_T002_RBend_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e = m.AddRBend("rb1", length=1, angle=30/180.*_np.pi)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T002_RBend_coordinates.json")

    # return c

def test_T002_RBend_poleface_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e = m.AddRBend("rb1", length=1, angle=45/180.*_np.pi, e1=45/180.*_np.pi, e2=45/180.*_np.pi)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T002_RBend_poleface_coordinates.json")

    # return c

def test_T002_RBend_many_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e1 = m.AddRBend("rb1", length=1, angle=30/180.*_np.pi)
    e2 = m.AddRBend("rb2", length=1, angle=30/180.*_np.pi)
    e3 = m.AddRBend("rb3", length=1, angle=30/180.*_np.pi)

    e4 = m.AddDrift("d1", length=1)
    e5 = m.AddDrift("d2", length=1)
    e6 = m.AddDrift("d3", length=1)
    e7 = m.AddDrift("d4", length=1)


    c = _pfbl.Coordinates.Coordinates()
    c.Append(e4)
    c.Append(e1)
    c.Append(e5)
    c.Append(e2)
    c.Append(e6)
    c.Append(e3)
    c.Append(e7)

    c.Build()
    c.SaveJSON("T002_RBend_many_coordinates.json")

    # return c

def test_T002_RBend_dogleg_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e1 = m.AddRBend("rb1", length=1, angle=30/180.*_np.pi)
    e2 = m.AddRBend("rb2", length=1, angle=-30/180.*_np.pi)

    e4 = m.AddDrift("d1", length=1)
    e5 = m.AddDrift("d2", length=1)
    e6 = m.AddDrift("d3", length=1)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e4)
    c.Append(e1)
    c.Append(e5)
    c.Append(e2)
    c.Append(e6)

    c.Build()
    c.SaveJSON("T002_RBend_dogleg_coordinates.json")

    # return c

def test_T002_RBend_tilt_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e = m.AddRBend("rb1", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T002_RBend_tilt_coordinates.json")

    # return c

def test_T002_RBend_tilt_many_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e1 = m.AddRBend("rb1", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)
    e2 = m.AddRBend("rb2", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)
    e3 = m.AddRBend("rb3", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)

    e4 = m.AddDrift("d1", length=1)
    e5 = m.AddDrift("d2", length=1)
    e6 = m.AddDrift("d3", length=1)
    e7 = m.AddDrift("d4", length=1)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e4)
    c.Append(e1)
    c.Append(e5)
    c.Append(e2)
    c.Append(e6)
    c.Append(e3)
    c.Append(e7)

    c.Build()
    c.SaveJSON("T002_RBend_tilt_many_coordinates.json")

    #return c

def test_T002_RBend_bend_tilt_many_coordinates() :
    m = _pfbl.BuilderNew.Machine()

    rb1 = m.AddRBend("rb1", length=1, angle=30/180.*_np.pi)
    rb2 = m.AddRBend("rb2", length=1, angle=30/180.*_np.pi)
    rb3 = m.AddRBend("rb3", length=1, angle=30/180.*_np.pi)

    rbt1 = m.AddRBend("rbt1", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)
    rbt2 = m.AddRBend("rbt2", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)
    rbt3 = m.AddRBend("rbt3", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)

    d1 = m.AddDrift("d1", length=1)
    d2 = m.AddDrift("d2", length=1)
    d3 = m.AddDrift("d3", length=1)
    d4 = m.AddDrift("d4", length=1)
    d5 = m.AddDrift("d5", length=1)
    d6 = m.AddDrift("d6", length=1)
    d7 = m.AddDrift("d7", length=1)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(d1)
    c.Append(rb1)
    c.Append(d2)
    c.Append(rb2)
    c.Append(d3)
    c.Append(rb3)
    c.Append(d4)

    c.Append(rbt1)
    c.Append(d5)
    c.Append(rbt2)
    c.Append(d6)
    c.Append(rbt3)
    c.Append(d7)

    c.Build()
    c.SaveJSON("T002_RBend_bend_tilt_many_coordinates.json")

    # return c

def test_T003_SBend_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e = m.AddSBend("sb1", length=1, angle=30/180.*_np.pi)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T003_SBend_coordinates.json")

    # return c

def test_T003_SBend_many_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e1 = m.AddSBend("sb1", length=1, angle=30/180.*_np.pi)
    e2 = m.AddSBend("sb2", length=1, angle=30/180.*_np.pi)
    e3 = m.AddSBend("sb3", length=1, angle=30/180.*_np.pi)

    e4 = m.AddDrift("d1", length=1)
    e5 = m.AddDrift("d2", length=1)
    e6 = m.AddDrift("d3", length=1)
    e7 = m.AddDrift("d4", length=1)


    c = _pfbl.Coordinates.Coordinates()
    c.Append(e4)
    c.Append(e1)
    c.Append(e5)
    c.Append(e2)
    c.Append(e6)
    c.Append(e3)
    c.Append(e7)

    c.Build()
    c.SaveJSON("T003_SBend_many_coordinates.json")

    # return c

def test_T003_SBend_dogleg_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e1 = m.AddSBend("sb1", length=1, angle=30/180.*_np.pi)
    e2 = m.AddSBend("sb2", length=1, angle=-30/180.*_np.pi)

    e4 = m.AddDrift("d1", length=1)
    e5 = m.AddDrift("d2", length=1)
    e6 = m.AddDrift("d3", length=1)


    c = _pfbl.Coordinates.Coordinates()
    c.Append(e4)
    c.Append(e1)
    c.Append(e5)
    c.Append(e2)
    c.Append(e6)

    c.Build()
    c.SaveJSON("T003_SBend_dogleg_coordinates.json")

    # return c

def test_T003_SBend_tilt_many_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e1 = m.AddSBend("sb1", length=1, angle=30.0/180.*_np.pi, tilt=_np.pi/2)
    e2 = m.AddSBend("sb2", length=1, angle=30.0/180.*_np.pi, tilt=_np.pi/2)
    e3 = m.AddSBend("sb3", length=1, angle=30.0/180.*_np.pi, tilt=_np.pi/2)

    e4 = m.AddDrift("d1", length=1)
    e5 = m.AddDrift("d2", length=1)
    e6 = m.AddDrift("d3", length=1)
    e7 = m.AddDrift("d4", length=1)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e4)
    c.Append(e1)
    c.Append(e5)
    c.Append(e2)
    c.Append(e6)
    c.Append(e3)
    c.Append(e7)

    c.Build()
    c.SaveJSON("T003_SBend_tilt_many_coordinates.json")

    # return c

def test_T003_SBend_tilt_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e = m.AddRBend("sb1", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T003_SBend_tilt_coordinates.json")

    # return c

def test_T004_Quad_coordinates() :
    m = _pfbl.BuilderNew.Machine()
    e1 = m.AddDrift("d1",length=1.0)
    e2 = m.AddQuadrupole("q1",length=1.0, k1=0.1)
    e3 = m.AddDrift("d2",length=1.0)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e1)
    c.Append(e2)
    c.Append(e3)

    c.Build()
    c.SaveJSON("T004_Quad_coordinates.json")

    # return c
    
