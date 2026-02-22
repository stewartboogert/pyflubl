import numpy as _np
import pyg4ometry as _pyg4
from pyg4ometry.transformation import tbxyz2matrix as _tbxyz2matrix

from .Options import Options as _Options

def _PlaneLineIntersection(planePoint, planeNormal, linePoint, lineDirection):
    # Calculate the dot product of the plane normal and the line direction
    dot_product = _np.dot(planeNormal, lineDirection)

    # Check if the line is parallel to the plane
    if abs(dot_product) < 1e-6:
        return None  # No intersection, line is parallel to the plane

    # Calculate the distance from the line point to the plane
    distance = _np.dot(planeNormal, planePoint - linePoint) / dot_product

    # Calculate the intersection point
    intersection_point = linePoint + distance * lineDirection

    return intersection_point

def _MakeGeant4GenericTrap_PoleFaceAngles(g4registry = None,
                                          name = "generic_trap_pole_face_angles",
                                          halflength = 500,
                                          xhalfwidth = 50,
                                          yhalfwidth = 50,
                                          e1=0,
                                          e2=0):

        # No registry, so create one
        if not g4registry:
            g4registry = _pyg4.geant4.Registry()

        p1x = -halflength + yhalfwidth * _np.tan(e1)
        p1y = yhalfwidth
        p2x = -halflength - yhalfwidth * _np.tan(e1)
        p2y = -yhalfwidth
        p3x =  halflength - yhalfwidth * _np.tan(e2)
        p3y = -yhalfwidth
        p4x =  halflength + yhalfwidth * _np.tan(e2)
        p4y =  yhalfwidth
        p5x = p1x
        p5y = p1y
        p6x = p2x
        p6y = p2y
        p7x = p3x
        p7y = p3y
        p8x = p4x
        p8y = p4y
        z = xhalfwidth
        trapsolid    = _pyg4.geant4.solid.GenericTrap(name+"_solid",
                                                      p1x,p1y,
                                                      p2x,p2y,
                                                      p3x,p3y,
                                                      p4x,p4y,
                                                      p5x,p5y,
                                                      p6x,p6y,
                                                      p7x,p7y,
                                                      p8x,p8y,
                                                      z,g4registry)

        return trapsolid

def _MakeGeant4GenericTrap_NormalVector(g4registry = None,
                                        name = "generic_trap_normal_vector",
                                        halflength=1000,
                                        xhalfwidth=250,
                                        yhalfwidth=250,
                                        faceNormalIn = _np.array([0,0,-1]),
                                        faceNormalOut = _np.array([0,0,1]),):

    # No registry, so create one
    if not g4registry:
        g4registry = _pyg4.geant4.Registry()

    # normalise face normals
    faceNormalIn = faceNormalIn/ _np.linalg.norm(faceNormalIn)
    faceNormalOut = faceNormalOut / _np.linalg.norm(faceNormalOut)

    zxrot = _tbxyz2matrix([0,_np.pi/2,0])

    print(zxrot)

    # rotate face normals to be in y directoin
    faceNormalIn = zxrot @ faceNormalIn
    faceNormalOut = zxrot @ faceNormalOut

    print("face normals")
    print(faceNormalIn)
    print(faceNormalOut)

    # point on face place is in y direction
    facePointIn = zxrot @ _np.array([0,0,-halflength])
    facePointOut = zxrot @ _np.array([0,0, halflength])

    print("face points")
    print(facePointIn)
    print(facePointOut)

    p1_pos = _np.array([0, -xhalfwidth,  yhalfwidth])
    p2_pos = _np.array([0, xhalfwidth,  yhalfwidth])
    p3_pos = _np.array([0, -xhalfwidth, -yhalfwidth])
    p4_pos = _np.array([0, xhalfwidth, -yhalfwidth])
    x_dir = _np.array([1,0,0])

    p1 = _PlaneLineIntersection(facePointIn, faceNormalIn, p1_pos, x_dir)
    p2 = _PlaneLineIntersection(facePointIn, faceNormalIn, p2_pos, x_dir)
    p3 = _PlaneLineIntersection(facePointOut, faceNormalOut, p1_pos, x_dir)
    p4 = _PlaneLineIntersection(facePointOut, faceNormalOut, p2_pos, x_dir)

    p5 = _PlaneLineIntersection(facePointIn, faceNormalIn, p3_pos, x_dir)
    p6 = _PlaneLineIntersection(facePointIn, faceNormalIn, p4_pos, x_dir)
    p7 = _PlaneLineIntersection(facePointOut, faceNormalOut, p3_pos, x_dir)
    p8 = _PlaneLineIntersection(facePointOut, faceNormalOut, p4_pos, x_dir)

    trapsolid = _pyg4.geant4.solid.GenericTrap(name + "_solid",
                                               p1[0], p1[1],
                                               p2[0], p2[1],
                                               p4[0], p4[1],
                                               p3[0], p3[1],
                                               p5[0], p5[1],
                                               p6[0], p6[1],
                                               p8[0], p8[1],
                                               p7[0], p7[1],
                                               yhalfwidth,
                                               g4registry)

    print("points +z")
    print(p1)
    print(p2)
    print(p3)
    print(p4)
    print("points -z")
    print(p5)
    print(p6)
    print(p7)
    print(p8)

    return trapsolid

def MakeBeamPipeCircular(g4registry = None,
                         name = "circular_beam_pipe",
                         length = 1000,
                         beamPipeRadius = _Options().beampipeRadius,
                         beamPipeThickness = _Options().beampipeThickness,
                         beamPipeMaterialName = _Options().beampipeMaterial,
                         vacuumMaterialName = _Options().vacuumMaterial,
                         faceNormalIn = _np.array([0,0,-1]),
                         faceNormalOut = _np.array([0,0,1])):

    # No registry, so create one
    if g4registry is None:
        g4registry = _pyg4.geant4.Registry()

    # normalise face normals
    faceNormalIn = faceNormalIn/ _np.linalg.norm(faceNormalIn)
    faceNormalOut = faceNormalOut / _np.linalg.norm(faceNormalOut)

    # fake materials
    vacuumMaterial = _pyg4.geant4.MaterialSingleElement(name=vacuumMaterialName, atomic_number=1, atomic_weight=1,
                                                        density=1)
    beampipeMaterial = _pyg4.geant4.MaterialSingleElement(name=beamPipeMaterialName, atomic_number=1, atomic_weight=1,
                                                          density=1)

    # make actual beampipe
    bpsolid = _pyg4.geant4.solid.CutTubs(name + "_bp_solid",
                                         0, beamPipeRadius + beamPipeThickness, length,
                                         0, _np.pi * 2,
                                         faceNormalIn,
                                         faceNormalOut,
                                         g4registry)
    bplogical = _pyg4.geant4.LogicalVolume(bpsolid, beampipeMaterial, name + "_bp_lv", g4registry)

    vacsolid = _pyg4.geant4.solid.CutTubs(name + "_vac_solid",
                                          0, beamPipeRadius, length,
                                          0, _np.pi * 2,
                                          faceNormalIn,
                                          faceNormalOut,
                                          g4registry)
    vaclogical = _pyg4.geant4.LogicalVolume(vacsolid, vacuumMaterial, name + "_cav_lv", g4registry)
    vacphysical = _pyg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], vaclogical, name + "_vac_pv", bplogical, g4registry)

    return [bplogical, vacphysical]

def MakeBeamPipeElliptical(g4reg):
    pass

def MakeDrift(g4registry = None,
              name = "drift",
              length = 1000,
              beamPipeRadius = _Options().beampipeRadius,
              beamPipeThickness = _Options().beampipeThickness,
              beamPipeMaterialName = _Options().beampipeMaterial,
              vacuumMaterialName = _Options().vacuumMaterial,
              outerMaterialName = _Options().outerMaterial,
              outerHorizontalSize = _Options().outerHorizontalSize,
              outerVerticalSize = _Options().outerVerticalSize,
              faceNormalIn = _np.array([0,0,-1]),
              faceNormalOut = _np.array([0,0,1])):

    # No registry, so create one
    if g4registry is None:
        localreg = True
        g4registry = _pyg4.geant4.Registry()

    outerMaterial = _pyg4.geant4.MaterialSingleElement(name=outerMaterialName, atomic_number=1, atomic_weight=1,
                                                       density=1)

    #outerSolid = _MakeGeant4GenericTrap_NormalVector(g4registry, name, length/2,
    #                                                 outerHorizontalSize/2, outerVerticalSize/2,
    #                                                 faceNormalIn, faceNormalOut)
    outerSolid = _MakeGeant4GenericTrap_PoleFaceAngles(g4registry, name, length/2,
                                                       outerHorizontalSize/2, outerVerticalSize/2,
                                                       e1=-_np.pi/4, e2=_np.pi/4)

    outerLogical = _pyg4.geant4.LogicalVolume(outerSolid, outerMaterial, name + "_outer_lv", g4registry)

    if localreg :
        g4registry.setWorld(outerLogical)

    return outerLogical

def DrawGeometry(logical) :
    v = _pyg4.visualisation.VtkViewerNew()
    v.addLogicalVolume(logical)
    v.buildPipelinesAppend()
    v.view()

def SaveGeometry(g4registry, filename) :
    w = _pyg4.gdml.Writer()
    w.addDetector(g4registry)
    w.write(filename)