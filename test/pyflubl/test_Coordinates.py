import pyflubl as _pfbl
import numpy as _np
import os as _os

def test_T001_drift_coordinates() :
    m = _pfbl.Builder.Machine()
    e = m.AddDrift("d1", length=1)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T001_drift_coordinates.json")

    return c

def test_T001_drift_many_coordinates() :
    m = _pfbl.Builder.Machine()
    e1 = m.AddDrift("d1", length=1)
    e2 = m.AddDrift("d2", length=2)
    e3 = m.AddDrift("d3", length=3)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e1)
    c.Append(e2)
    c.Append(e3)

    c.Build()
    c.SaveJSON("T001_drift_many_coordinates.json")

    return c

def test_T002_rbend_coordinates() :
    m = _pfbl.Builder.Machine()
    e = m.AddRBend("rb1", length=1, angle=30/180.*_np.pi)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T002_rbend_coordinates.json")

    return c

def test_T002_rbend_poleface_coordinates() :
    m = _pfbl.Builder.Machine()
    e = m.AddRBend("rb1", length=1, angle=45/180.*_np.pi, e1=45/180.*_np.pi, e2=45/180.*_np.pi)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T002_rbend_poleface_coordinates.json")

    return c

def test_T002_rbend_many_coordinates() :
    m = _pfbl.Builder.Machine()
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
    c.SaveJSON("T002_rbend_many_coordinates.json")

    return c

def test_T002_rbend_dogleg_coordinates() :
    m = _pfbl.Builder.Machine()
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
    c.SaveJSON("T002_rbend_dogleg_coordinates.json")

    return c

def test_T002_rbend_tilt_coordinates() :
    m = _pfbl.Builder.Machine()
    e = m.AddRBend("rb1", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T002_rbend_tilt_coordinates.json")

    return c

def test_T002_rbend_tilt_many_coordinates() :
    m = _pfbl.Builder.Machine()
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
    c.SaveJSON("T002_rbend_tilt_many_coordinates.json")

    return c

def test_T003_sbend_coordinates() :
    m = _pfbl.Builder.Machine()
    e = m.AddSBend("sb1", length=1, angle=30/180.*_np.pi)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T003_sbend_coordinates.json")

    return c

def test_T003_sbend_many_coordinates() :
    m = _pfbl.Builder.Machine()
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
    c.SaveJSON("T003_sbend_many_coordinates.json")

    return c

def test_T003_sbend_dogleg_coordinates() :
    m = _pfbl.Builder.Machine()
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
    c.SaveJSON("T003_sbend_dogleg_coordinates.json")

    return c

def test_T003_sbend_tilt_many_coordinates() :
    m = _pfbl.Builder.Machine()
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
    c.SaveJSON("T003_sbend_tilt_many_coordinates.json")

    return c

def test_T003_sbend_tilt_coordinates() :
    m = _pfbl.Builder.Machine()
    e = m.AddRBend("sb1", length=1, angle=30/180.*_np.pi, tilt=_np.pi/2)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T003_sbend_tilt_coordinates.json")

    return c

def test_T004_quad_coordinates() :
    m = _pfbl.Builder.Machine()
    e1 = m.AddDrift("d1",length=1.0)
    e2 = m.AddQuadrupole("q1",length=1.0, k1=0.1)
    e3 = m.AddDrift("d2",length=1.0)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e1)
    c.Append(e2)
    c.Append(e3)

    c.Build()
    c.SaveJSON("T004_quad_coordinates.json")

    return c
    
