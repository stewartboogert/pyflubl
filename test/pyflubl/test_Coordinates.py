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
    e = m.AddRBend("rb1", length=1, angle=0.05)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T002_rbend_coordinates.json")

    return c

def test_T002_rbend_tilt_coordinates() :
    m = _pfbl.Builder.Machine()
    e = m.AddRBend("rb1", length=1, angle=0.05, tilt=_np.pi/2)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T002_rbend_tilt_coordinates.json")

    return c

def test_T003_sbend_coordinates() :
    m = _pfbl.Builder.Machine()
    e = m.AddRBend("sb1", length=1, angle=0.05)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T003_sbend_coordinates.json")

    return c

def test_T003_sbend_tilt_coordinates() :
    m = _pfbl.Builder.Machine()
    e = m.AddRBend("sb1", length=1, angle=0.05, tilt=_np.pi/2)

    c = _pfbl.Coordinates.Coordinates()
    c.Append(e)

    c.Build()
    c.SaveJSON("T003_sbend_tilt_coordinates.json")

    return c