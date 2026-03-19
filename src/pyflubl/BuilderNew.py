from collections import defaultdict as _defaultdict
import numpy as _np
import json as _json
import pprint as _pprint

from .Coordinates import Coordinates as _Coordinates
from .Options import Options as _Options
from .Element import Element as _Element
from .Element import ElementGap as _ElementGap
from .Element import ElementCustomG4 as _ElementCustomG4
from .Element import ElementCustomFluka as _ElementCustomFluka
from .GeometryGeant4 import PlacementType as _PlacementType
from .GeometryGeant4 import MakeOuterTrapezoid as _MakeOuterTrapezoid
from .GeometryGeant4 import MakeBeamPipeCircular as _MakeBeamPipeCircular
from .GeometryGeant4 import MakeTarget as _MakeTarget
from .GeometryGeant4 import MakeRCol as _MakeRCol
from .GeometryGeant4 import MakeECol as _MakeECol
from .GeometryGeant4 import MakeJCol as _MakeJCol
from .GeometryGeant4 import MakeShield as _MakeShield
from .GeometryGeant4 import MakeDump as _MakeDump
from .GeometryGeant4 import MakeWireScanner as _MakeWireScanner

import pyg4ometry as _pyg4
from pyg4ometry.fluka.directive import rotoTranslationFromTra2 as _rotoTranslationFromTra2
from pyg4ometry.convert.geant42Fluka import geant4PhysicalVolume2Fluka as _geant4PhysicalVolume2Fluka
from pyg4ometry.transformation import matrix2tbxyz as _matrix2tbxyz
from pyg4ometry.transformation import tbxyz2matrix as _tbxyz2matrix
from pyg4ometry.transformation import tbxyz2axisangle as _tbxyz2axisangle


class Machine(_Coordinates) :
    def __init__(self, bakeTransforms = True, verbose = False) :
        super().__init__()

        # store if transforms are baked into bodies or rotdefis used
        self.bakeTransforms = bakeTransforms

        # verbose debugging information
        self.verbose = verbose

        # finished creation
        self.finished = False

        # element prototypes
        self.prototypes = {}

        # options (a.k.a defaults)
        self.options = _Options()

        # total length of machine
        self.length = 0

        # extent of machine in x,y,z
        self.maxx = 0.0
        self.maxy = 0.0
        self.maxz = 0.0

        # geometry registries (will be populated when MakeFlukaModel is called)
        self.g4registry = None
        self.flukaregistry = None

        # element to book-keeping-dict information
        self.elementBookkeeping = _defaultdict()

        # persistent book keeping
        self.nameRegion = {}
        self.regionnumber_regionname = {}
        self.regionnumber_element = {}
        self.regionname_regionnumber = {}
        self.volume_regionname = {}
        self.regionname_volume = {}
        self.usrbinnumber_usrbininfo = {}
        self.samplernames_samplernumber= {}

        # fluka indices
        self.flukanamecount = 0
        self.flukamgncount = 0     # number of magnetic field ROT-DEF placements
        self.flukabincount = 0

        # fluka control cards
        self.beam = None
        self.beam1 = None
        self.beampos = None
        self.beamaxes = None
        self.defaults = None
        self.elcfield = None
        self.title = None
        self.fglobal = None
        self.mgnfield = []
        self.mgncreat = []
        self.mgndata = []
        self.rotprbin = []
        self.randomiz = None
        self.source = None
        self.start = None
        self.usrbin = []
        self.userdump = []
        self.usricall = None
        self.usrocall = None

    def AddDrift(self,name, length, **kwargs):
        allowed_keys = _Element._beampipe_allowed_keys + \
                       _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys
        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="drift", length=length, **kwargs)
        self.Append(e)
        return e

    def AddRBend(self, name, length,  **kwargs):
        allowed_keys = _Element._beampipe_allowed_keys + \
                       _Element._outer_allowed_keys + \
                       _Element._rbend_allowed_keys + \
                       _Element._tiltshift_allowed_keys
        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)

        kwargs['outerE1'] = -kwargs['e1']
        kwargs['outerE2'] = -kwargs['e2']

        e = _Element(name=name, category="rbend", length=length, **kwargs)
        self.Append(e)
        return e

    def AddSBend(self, name, length, **kwargs):
        allowed_keys = _Element._beampipe_allowed_keys + \
                       _Element._outer_allowed_keys + \
                       _Element._sbend_allowed_keys + \
                       _Element._tiltshift_allowed_keys

        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)

        # need to set the outer trap angles for Sbend
        kwargs['outerE1'] = -kwargs['angle']/2 - kwargs['e1']
        kwargs['outerE2'] = -kwargs['angle']/2 - kwargs['e2']

        e = _Element(name=name, category="sbend", length = length, **kwargs)
        self.Append(e)
        return e

    def AddSBendSplit(self, name, length, nsplit=10, **kwargs):
        angle = kwargs.pop('angle')/nsplit
        length = length/nsplit

        for i in range(0,nsplit):
            self.AddSBend(name+"_split_"+str(i), length, angle = angle, **kwargs)

    def AddQuadrupole(self, name, length, **kwargs):
        allowed_keys = _Element._beampipe_allowed_keys + \
                       _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys + \
                       _Element._quadrupole_allowed_keys

        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="quadrupole", length = length, **kwargs)
        self.Append(e)
        return e

    def AddTarget(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys + \
                       _Element._target_allowed_keys

        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="target", length = length, **kwargs)
        self.Append(e)
        return e

    def AddRCol(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys + \
                       _Element._rcol_allowed_keys
        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="rcol", length = length, **kwargs)
        self.Append(e)
        return e

    def AddECol(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys + \
                       _Element._ecol_allowed_keys
        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="ecol", length = length, **kwargs)
        self.Append(e)
        return e

    def AddJCol(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys + \
                       _Element._jcol_allowed_keys
        self._CheckElementKwargs(kwargs,allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="jcol", length = length, **kwargs)
        self.Append(e)
        return e

    def AddShield(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys + \
                       _Element._beampipe_allowed_keys + \
                       _Element._shield_allowed_keys
        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="shield", length = length, **kwargs)
        self.Append(e)
        return e

    def AddDump(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys + \
                       _Element._target_allowed_keys

        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="dump", length = length, **kwargs)
        self.Append(e)
        return e

    def AddWireScanner(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys + \
                       _Element._beampipe_allowed_keys + \
                       _Element._wirescanner_allowed_keys

        self._CheckElementKwargs(kwargs,allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="wirescanner", length = length, **kwargs)
        self.Append(e)
        return e

    def AddGap(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._tiltshift_allowed_keys
        self._CheckElementKwargs(kwargs,allowed_keys)
        self._SetDefaultElementKwargs(kwargs,allowed_keys)
        e = _Element(name, category="gap", length = length, **kwargs)
        self.Append(e)
        return e

    def AddCustomG4(self, name, length, containerLV, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._customg4_allowed_keys + \
                       _Element._customg4file_allowed_keys + \
                       _Element._tiltshift_allowed_keys
        self._CheckElementKwargs(kwargs,allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)
        e = _Element(name=name, category="customG4", length = length, **kwargs)
        #e = _ElementCustomG4(name, length, containerLV, **kwargs)
        self.Append(e)
        return e

    def AddCustomG4File(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._customg4file_allowed_keys + \
                       _Element._tiltshift_allowed_keys
        self._CheckElementKwargs(kwargs,allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)

        geometry_file = kwargs['geometryFile']
        lv_name = kwargs['lvName']

        # registry for converter
        g4registry = self._GetGeant4Registry(True)

        # load file
        reader = _pyg4.gdml.Reader(geometry_file, registryIn = g4registry)
        lv = g4registry.logicalVolumeDict[lv_name]

        self.AddCustomG4(name,length, containerLV = lv, **kwargs)

    def AddCustomFluka(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys +\
                       _Element._customfluka_allowed_keys + \
                       _Element._customflukafile_allowed_keys
        self._CheckElementKwargs(kwargs,allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)

        e = _Element(name=name,
                     category="customFluka",
                     length=length,
                     **kwargs)
        self.Append(e)
        return e

    def AddCustomFlukaFile(self, name, length, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._customflukafile_allowed_keys
        self._CheckElementKwargs(kwargs,_Element._customflukafile_allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)

        geometry_file = kwargs['geometryFile']
        outer_bodies = kwargs['customOuterBodies']
        region_names = kwargs['customRegions']

        reader = _pyg4.fluka.Reader(geometry_file)
        registry = reader.getRegistry()

        if isinstance(outer_bodies, str) :
            outer_bodies = [registry.bodyDict[k] for k in outer_bodies.split()]
        elif isinstance(outer_bodies, list) :
            outer_bodies = [registry.bodyDict[k] for k in outer_bodies]

        if isinstance(region_names, str) :
            regions = [registry.regionDict[k] for k in region_names.split()]
        elif isinstance(region_names, list) :
            regions = [registry.regionDict[k] for k in region_names]

        kwargs['geometryFile'] = geometry_file
        kwargs['customOuterBodies'] = outer_bodies
        kwargs['customRegions'] = regions

        self.AddCustomFluka(name,length,flukaRegistry=registry, **kwargs)

    def AddLatticeInstance(self, name, prototypeName):
        e = _Element(name=name,
                     category="lattice_instance",
                     length=self.prototypes[prototypeName].length,
                     prototypeName=prototypeName)
        self.Append(e)
        return e

    def AddLatticePrototype(self, name, length, **kwargs):
        e = _Element(name=name,
                     category="lattice_prototype",
                     length = length,
                     **kwargs)
        # save in prototype dict
        # transformation to be populated when built
        self.prototypes[name] = {"element":e, "rotation":None, "translation":None}
        return e

    def AddSamplerPlane(self, name, length = None, **kwargs):
        allowed_keys = _Element._outer_allowed_keys + \
                       _Element._sampler_plane_allowed_keys + \
                       _Element._tiltshift_allowed_keys
        self._CheckElementKwargs(kwargs, allowed_keys)
        self._SetDefaultElementKwargs(kwargs, allowed_keys)

        # deftault sampler length
        if not length:
            length = self.options.samplerLength

        e = _Element(name=name, category="sampler_plane", length = length, **kwargs)
        self.Append(e)

        # Add bookkeeping information
        self.samplernames_samplernumber[name] = len(self.samplernames_samplernumber)

    def AddScoringHistogram(self):
        pass

    def AddScoringMesh(self):
        pass

    def _CheckElementKwargs(self, kwargs, allowed_keys):
        for key in kwargs:
            if key not in allowed_keys:
                raise TypeError(f"Unexpected keyword argument: {key}")

    def _SetDefaultElementKwargs(self, kwargs, allowed_keys):
        for ak in allowed_keys :
            if ak not in kwargs :
                if ak == "vacuumMaterial" :
                    kwargs[ak] = self.options.vacuumMaterial
                elif ak == "beampipeMaterial" :
                    kwargs[ak] = self.options.beampipeMaterial
                elif ak == "beampipeRadius" :
                    kwargs[ak] = self.options.beampipeRadius
                elif ak == "beampipeThickness" :
                    kwargs[ak] = self.options.beampipeThickness
                elif ak == "outerHorizontalSize" :
                    kwargs[ak] = self.options.outerHorizontalSize
                elif ak == "outerVerticalSize" :
                    kwargs[ak] = self.options.outerVerticalSize
                elif ak == "outerMaterial" :
                    kwargs[ak] = self.options.outerMaterial
                elif ak == "outerE1" :
                    kwargs[ak] = 0.0
                elif ak == "outerE2" :
                    kwargs[ak] = 0.0
                elif ak == "outerP1" :
                    kwargs[ak] = 0.0
                elif ak == "outerP2" :
                    kwargs[ak] = 0.0
                elif ak == "e1" :
                    kwargs[ak] = 0.0
                elif ak == "e2" :
                    kwargs[ak] = 0.0
                elif ak == "offsetX" :
                    kwargs[ak] = 0.0
                elif ak == "offsetY" :
                    kwargs[ak] = 0.0
                elif ak  == "tilt" :
                    kwargs[ak] = 0.0
                elif ak == "xsize" :
                    kwargs[ak] = 0.0
                elif ak == "ysize" :
                    kwargs[ak] = 0.0
                elif ak == "xsizeLeft" :
                    kwargs[ak] = 0.0
                elif ak == "xsizeRight" :
                    kwargs[ak] = 0.0
                elif ak == "horizontalWidth" :
                    kwargs[ak] = self.options.outerHorizontalSize*0.95
                elif ak == "verticalWidth" :
                    kwargs[ak] = self.options.outerVerticalSize*0.95
                elif ak == "material" :
                    kwargs[ak] = "IRON"
                elif ak == "jawTiltLeft" :
                    kwargs[ak] = 0.0
                elif ak == "jawTiltRight" :
                    kwargs[ak] = 0.0
                elif ak == "apertureType" :
                    kwargs[ak] = "circular"
                elif ak == "wireDiameter" :
                    kwargs[ak] = 5
                elif ak == "wireLength" :
                    kwargs[ak] = 25
                elif ak == "wireMaterial" :
                    kwargs[ak] = "IRON"
                elif ak == "wireAngle" :
                    kwargs[ak] = 0.0
                elif ak == "wireOffsetX" :
                    kwargs[ak] = 0.0
                elif ak == "wireOffsetY" :
                    kwargs[ak] = 0.0
                elif ak == "wireOffsetZ" :
                    kwargs[ak] = 0.0
                elif ak == "samplerMaterial" :
                    kwargs[ak] = self.options.samplerMaterial
                elif ak == "samplerLength" :
                    kwargs[ak] = self.options.samplerLength
                elif ak == "samplerDiameter" :
                    kwargs[ak] = self.options.samplerDiameter
                elif ak == "convertMaterials" :
                    kwargs[ak] = True
                else :
                    pass

    def AddBeam(self, beam):
        self.beam = beam

    def AddBeampos(self, beampos):
        self.beampos = beampos

    def AddBeamaxes(self, beamaxes):
        self.beamaxes = beamaxes

    def AddDefaults(self, defaults):
        self.defaults = defaults

    def AddElcfield(self, elcfield):
        self.elcfield = elcfield

    def AddGlobal(self, fglobal):
        self.fglobal = fglobal

    def AddMgnfield(self, mgnfield):
        self.mgnfield.append(mgnfield)

    def AddMgncreat(self, mgncreat):
        self.mgncreat.append(mgncreat)

    def AddMgndata(self, mgndata):
        self.mgndata.append(mgndata)

    def AddRotprbin(self, rotprbin):
        self.rotprbin.append(rotprbin)

    def AddRandomiz(self, randomiz):
        self.randomiz = randomiz

    def AddSource(self,source):
        self.source = source

    def AddStart(self, start):
        self.start = start

    def AddTitle(self, title):
        self.title = title

    def AddUsrbin(self, usrbin, rotmat = _np.array([[1,0,0],[0,1,0],[0,0,1]]), translation = _np.array([0,0,0])):
        # TODO reimplement
        '''
        self.usrbin.append(usrbin)

        # Add bookkeeping information
        self._AddBookkeepingUsrbin(self.flukabincount, usrbin.name, rotmat, translation)

        # increment counter for added usrbin
        self.flukabincount += 1
        '''

    def AddUsrbinToElement(self, element, usrbin = None, scaleUsrbinToElement = False):
        # TODO reimplement
        '''
        # get element name
        if type(element) is str :
            element_name = element
        else :
            element_name = element.name

        # element index
        element_idx = list(self.elements.keys()).index(element_name)

        # get transformation
        element_rotmat = self.midrotationint[element_idx]
        element_rotmat_inv = _np.linalg.inv(element_rotmat)

        element_rot_inv = _matrix2tbxyz(element_rotmat_inv)
        element_translation = self.midint[element_idx]*1000
        element_translation_inv = - element_rotmat_inv @ element_translation

        # make rotdefi
        transformation_name = "TB"+format(self.flukabincount, "03")
        rdi = _rotoTranslationFromTra2(transformation_name,[element_rot_inv, element_translation_inv])
        if len(rdi) > 0 :
            self.flukaregistry.addRotoTranslation(rdi)

        # add ROTPRBIN
        rotprbin = _Rotprbin(storagePrecision=0,
                             rotDefi=transformation_name,
                             usrbinStart=usrbin.name)
        self.AddRotprbin(rotprbin)

        # add USRBIN
        self.AddUsrbin(usrbin, element_rotmat, element_translation)
        '''

    def AddUserdump(self, userdump):
        self.userdump.append(userdump)

    def AddUsricall(self, usricall):
        self.usricall = usricall

    def AddUsrocall(self, usrocall):
        self.usrocall = usrocall

    def _MakeBookkeepingInfo(self):
        if self.verbose :
            print("pyflubl.BuilderNew.Machine._MakeBookkeepingInfo: Making bookkeeping information...")

        self.finished = True

        # loop over elements and put S location
        for i, e in enumerate(self.elements):
            self.elementBookkeeping[e]["S"] = self.s_mid[i]
            self.elementBookkeeping[e]["length"] = self.elements[e].length

        # region number to name
        for i, r in enumerate(self.flukaregistry.regionDict) :
            self.regionnumber_regionname[i+1] = self.flukaregistry.regionDict[r].name
            self.regionname_regionnumber[self.flukaregistry.regionDict[r].name] = i+1

            self.volume_regionname[self.flukaregistry.regionDict[r].comment] = self.flukaregistry.regionDict[r].name
            self.regionname_volume[self.flukaregistry.regionDict[r].name] = self.flukaregistry.regionDict[r].comment

            # loop over all elements and find reference to the region in an element
            for element_name, element_info in self.elementBookkeeping.items() :
                if self.flukaregistry.regionDict[r].name in element_info['flukaRegions'] :
                    self.regionnumber_element[i+1] = element_name

    def _WriteBookkeepingInfo(self, fileName="output.json", pretty=False):

        if not self.finished :
            self._MakeBookkeepingInfo()

        jsonDumpDict = {}
        jsonDumpDict["elements"] = dict(self.elementBookkeeping)
        jsonDumpDict["samplernames_samplernumber"] = self.samplernames_samplernumber
        jsonDumpDict["regionname_regionnumber"] = self.regionname_regionnumber
        jsonDumpDict["regionnumber_regionname"] = self.regionnumber_regionname
        jsonDumpDict["regionnumber_element"] = self.regionnumber_element
        jsonDumpDict["usrbinnumber_usrbininfo"] = self.usrbinnumber_usrbininfo

        if not pretty :
            with open(fileName, "w") as f:
                _json.dump(jsonDumpDict,f)
        else :
            # write json to file with human-friendly formatting
            pretty_json_str = _pprint.pformat(jsonDumpDict, compact=True).replace("'", '"')

            with open(fileName, 'w') as f:
                f.write(pretty_json_str)

    def Write(self, filename, prettyJSON = False):
        if self.verbose :
            print("pyflubl.BuilderNew.Machine.Write: Writing model to file...")

        if not self.flukaregistry :
            self.MakeFlukaModel()

        flukaINPFileName = filename+".inp"
        geant4GDMLFileName = filename+".gdml"
        bookkeepignFileName = filename+".json"

        if self.beam :
            self.beam.AddRegistry(self.flukaregistry)
        if self.beam1 :
            self.beam1.AddRegistry(self.flukaregistry)
        if self.beampos :
            self.beampos.AddRegistry(self.flukaregistry)
        if self.beamaxes :
            self.beamaxes.AddRegistry(self.flukaregistry)
        if self.defaults :
            self.defaults.AddRegistry(self.flukaregistry)
        if self.elcfield :
            self.elcfield.AddRegistry(self.flukaregistry)
        if self.fglobal:
            self.fglobal.AddRegistry(self.flukaregistry)
        if len(self.mgnfield) > 0 :
            for mf in self.mgnfield:
                mf.AddRegistry(self.flukaregistry)
        if len(self.mgncreat) > 0 :
            for mc in self.mgncreat:
                mc.AddRegistry(self.flukaregistry)
        if len(self.rotprbin) > 0 :
            for pr in self.rotprbin:
                pr.AddRegistry(self.flukaregistry)
        if self.randomiz :
            self.randomiz.AddRegistry(self.flukaregistry)
        if self.source :
            self.source.AddRegistry(self.flukaregistry)
        if self.start :
            self.start.AddRegistry(self.flukaregistry)
        if self.title:
            self.title.AddRegistry(self.flukaregistry)
        if len(self.usrbin) > 0 :
            for ub in self.usrbin:
                ub.AddRegistry(self.flukaregistry)
        if len(self.userdump) > 0 :
            for ud in self.userdump:
                ud.AddRegistry(self.flukaregistry)
        if self.usricall :
            self.usricall.AddRegistry(self.flukaregistry)
        if self.usrocall :
            self.usrocall.AddRegistry(self.flukaregistry)

        fw = _pyg4.fluka.Writer()
        fw.addDetector(self.flukaregistry)
        fw.write(flukaINPFileName)

        gw = _pyg4.gdml.Writer()
        gw.addDetector(self.g4registry)
        gw.write(geant4GDMLFileName)

        self._WriteBookkeepingInfo(bookkeepignFileName, pretty=prettyJSON)

    def __repr__(self):
        s = ''
        s += 'pyflubl.BuilderNew.Machine instance\n'
        s += str(len(self.sequence)) + ' items in sequence\n'
        s += str(len(self.elements)) + ' unique elements defined\n'
        return s

    def MakeFlukaModel(self):
        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaModel:")

        # make registries
        self.flukaregistry = self._GetFlukaRegistry(True)
        self.g4registry    = self._GetGeant4Registry(True)

        # build coordinates
        self.Build(circular=False)

        # initial world size
        extent = self.CalculateExtent()

        # sizes in cm
        xmax = max(abs(extent[0][0]), abs(extent[1][0]))*100 + 1000
        ymax = max(abs(extent[0][1]), abs(extent[1][1]))*100 + 1000
        zmax = max(abs(extent[0][2]), abs(extent[1][2]))*100 + 1000

        # make world region and surrounding black body
        self.MakeFlukaInitialGeometry(worldsize=[xmax,ymax,zmax],worldmaterial=self.options.worldMaterial)
        self.MakeGeant4InitialGeometry(worldsize=[2*xmax*10, 2*ymax*10, 2*zmax*10])

        # fix faces of elements
        # self._FixElementFaces(view=False)

        # make lattice prototypes
        for prototype in self.prototypes :
            pass

        # loop over elements in sequence
        # (r)rotation, (t)translation, (g)geom(t)ranslation,
        # (c)ubical(b)ounding,
        # (t)rapezoidal(b)ounding
        for name,r,t,gt,cb, tb in zip(self.sequence,self.rot_mid, self.arc_mid, self.cho_mid, self.cub_loc, self.tra_loc) :
            e = self.elements[name]

            # populate initial book keeping information
            if name not in self.elementBookkeeping:
                self.elementBookkeeping[name] = {}

            # make element
            self.ElementFactory(e, r, t, gt, cb, tb)

        # make book keeping info
        self._MakeBookkeepingInfo()

        return self.flukaregistry

    def MakeGeant4InitialGeometry(self, worldsize = [5000, 5000, 5000], worldMaterial = "G4_AIR"):
        worldSolid = _pyg4.geant4.solid.Box("world",worldsize[0], worldsize[1], worldsize[2], self.g4registry)
        self.worldLogical = _pyg4.geant4.LogicalVolume(worldSolid, worldMaterial, "worldLogical", self.g4registry)
        self.g4registry.setWorldVolume(self.worldLogical)

    def MakeFlukaInitialGeometry(self, worldsize = [250, 250, 250], worldmaterial = "AIR"):
        blackbody = _pyg4.fluka.RPP("BLKBODY",
                               -2*worldsize[0],2*worldsize[0],
                               -2*worldsize[1],2*worldsize[1],
                               -2*worldsize[2],2*worldsize[2],
                               transform=_rotoTranslationFromTra2("BBROTDEF",[[0,0,0],[0,0,0]],
                                                                  flukaregistry=self.flukaregistry),
                               flukaregistry=self.flukaregistry)

        worldbody = _pyg4.fluka.RPP("WORLD",
                               -1.5*worldsize[0],1.5*worldsize[0],
                               -1.5*worldsize[1],1.5*worldsize[1],
                               -1.5*worldsize[2],1.5*worldsize[2],
                               transform=_rotoTranslationFromTra2("BBROTDEF",[[0,0,0],[0,0,0]],
                                                                  flukaregistry=self.flukaregistry),
                               flukaregistry=self.flukaregistry)

        self.blackbodyzone = _pyg4.fluka.Zone()
        self.worldzone     = _pyg4.fluka.Zone()

        self.blackbodyzone.addIntersection(blackbody)
        self.blackbodyzone.addSubtraction(worldbody)

        self.worldzone.addIntersection(worldbody)

        self.blackbodyregion = _pyg4.fluka.Region("BLKHOLE")
        self.blackbodyregion.addZone(self.blackbodyzone)
        self.flukaregistry.addRegion(self.blackbodyregion)
        self.flukaregistry.addMaterialAssignments("BLCKHOLE",
                                                  "BLKHOLE")

        self.worldregion = _pyg4.fluka.Region("WORLD")
        self.worldregion.addZone(self.worldzone)
        self.flukaregistry.addRegion(self.worldregion)
        self.flukaregistry.addMaterialAssignments(worldmaterial,
                                                  "WORLD")

    def ElementFactory(self,
                       element,
                       rotation,
                       translation,
                       geomtranslation,
                       cubicalbound,
                       trapezoidalbound,
                       g4add = True,
                       fc = True):
        if self.verbose :
            print("pyflubl.BuilderNew.Machine.ElementFactory: Making FLUKA geometry for ", element.name, element.category)

        if element.category == "drift":
            return self.MakeFlukaDrift(name=element.name,
                                       element=element,
                                       rotation=rotation,
                                       translation=translation * 1000,
                                       geomtranslation=geomtranslation * 1000,
                                       cubicalbound=cubicalbound,
                                       trapezoidalbound=trapezoidalbound,
                                       geant4RegistryAdd=g4add,
                                       flukaConvert=fc)
        if element.category == "rbend":
            return self.MakeFlukaRBend(name=element.name,
                                       element=element,
                                       rotation=rotation,
                                       translation=translation * 1000,
                                       geomtranslation=geomtranslation * 1000,
                                       cubicalbound=cubicalbound,
                                       trapezoidalbound=trapezoidalbound,
                                       geant4RegistryAdd=g4add,
                                       flukaConvert=fc)
        if element.category == "sbend":
            return self.MakeFlukaSBend(name=element.name,
                                       element=element,
                                       rotation=rotation,
                                       translation=translation * 1000,
                                       geomtranslation=geomtranslation * 1000,
                                       cubicalbound=cubicalbound,
                                       trapezoidalbound=trapezoidalbound,
                                       geant4RegistryAdd=g4add,
                                       flukaConvert=fc)
        elif element.category == "quadrupole":
            return self.MakeFlukaQuadrupole(name=element.name,
                                           element=element,
                                           rotation=rotation,
                                           translation=translation * 1000,
                                           geomtranslation=geomtranslation * 1000,
                                           cubicalbound=cubicalbound,
                                           trapezoidalbound=trapezoidalbound,
                                           geant4RegistryAdd=g4add,
                                           flukaConvert=fc)
        elif element.category == "target":
            return self.MakeFlukaTarget(name=element.name,
                                        element=element,
                                        rotation=rotation,
                                        translation=translation * 1000,
                                        geomtranslation=geomtranslation * 1000,
                                        cubicalbound=cubicalbound,
                                        trapezoidalbound=trapezoidalbound,
                                        geant4RegistryAdd=g4add,
                                        flukaConvert=fc)
        elif element.category == "rcol":
            return self.MakeFlukaRCol(name=element.name,
                                      element=element,
                                      rotation=rotation,
                                      translation=translation * 1000,
                                      geomtranslation=geomtranslation * 1000,
                                      cubicalbound=cubicalbound,
                                      trapezoidalbound=trapezoidalbound,
                                      geant4RegistryAdd=g4add,
                                      flukaConvert=fc)
        elif element.category == "ecol":
            return self.MakeFlukaECol(name=element.name,
                                      element=element,
                                      rotation=rotation,
                                      translation=translation * 1000,
                                      geomtranslation=geomtranslation * 1000,
                                      cubicalbound=cubicalbound,
                                      trapezoidalbound=trapezoidalbound,
                                      geant4RegistryAdd=g4add,
                                      flukaConvert=fc)
        elif element.category == "jcol":
            return self.MakeFlukaJCol(name=element.name,
                                      element=element,
                                      rotation=rotation,
                                      translation=translation * 1000,
                                      geomtranslation=geomtranslation * 1000,
                                      cubicalbound=cubicalbound,
                                      trapezoidalbound=trapezoidalbound,
                                      geant4RegistryAdd=g4add,
                                      flukaConvert=fc)
        elif element.category == "shield":
            return self.MakeFlukaShield(name=element.name,
                                        element=element,
                                        rotation=rotation,
                                        translation=translation * 1000,
                                        geomtranslation=geomtranslation * 1000,
                                        cubicalbound=cubicalbound,
                                        trapezoidalbound=trapezoidalbound,
                                        geant4RegistryAdd=g4add,
                                        flukaConvert=fc)
        elif element.category == "dump":
            return self.MakeFlukaDump(name=element.name,
                                      element=element,
                                      rotation=rotation,
                                      translation=translation * 1000,
                                      geomtranslation=geomtranslation * 1000,
                                      cubicalbound=cubicalbound,
                                      trapezoidalbound=trapezoidalbound,
                                      geant4RegistryAdd=g4add,
                                      flukaConvert=fc)
        elif element.category == "wirescanner":
            return self.MakeFlukaWireScanner(name=element.name,
                                             element=element,
                                             rotation=rotation,
                                             translation=translation * 1000,
                                             geomtranslation=geomtranslation * 1000,
                                             cubicalbound=cubicalbound,
                                             trapezoidalbound=trapezoidalbound,
                                             geant4RegistryAdd=g4add,
                                             flukaConvert=fc)
        elif element.category == "gap":
            return self.MakeFlukaGap(name=element.name,
                                     element=element,
                                     rotation=rotation,
                                     translation=translation * 1000,
                                     geomtranslation=geomtranslation * 1000,
                                     cubicalbound=cubicalbound,
                                     trapezoidalbound=trapezoidalbound,
                                     geant4RegistryAdd=g4add,
                                     flukaConvert=fc)
        elif element.category == "customG4":
            return self.MakeFlukaCustomG4(name=element.name,
                                          element=element,
                                          rotation=rotation,
                                          translation=translation * 1000,
                                          geomtranslation=geomtranslation * 1000,
                                          cubicalbound=cubicalbound,
                                          trapezoidalbound=trapezoidalbound,
                                          geant4RegistryAdd=g4add,
                                          flukaConvert=fc)
        elif element.category == "customFluka":
            return self.MakeFlukaCustomFluka(name=element.name,
                                             element=element,
                                             rotation=rotation,
                                             translation=translation * 1000,
                                             geomtranslation=geomtranslation * 1000,
                                             cubicalbound=cubicalbound,
                                             trapezoidalbound=trapezoidalbound,
                                             flukaConvert=fc)
        elif element.category == "sampler_plane":
            return self.MakeFlukaSampler(name=element.name,
                                         element=element,
                                         rotation=rotation,
                                         translation=translation * 1000,
                                         geomtranslation=geomtranslation * 1000,
                                         cubicalbound=cubicalbound,
                                         trapezoidalbound=trapezoidalbound,
                                         geant4RegistryAdd=g4add,
                                         flukaConvert=fc)
        else :
            print("Element category not recognized: ", element.category)

    def MakeFlukaDrift(self,
                       name,
                       element,
                       rotation = _np.array([[1,0,0],[0,1,0],[0,0,1]]),
                       translation = _np.array([0,0,0]),
                       geomtranslation = _np.array([0,0,0]),
                       cubicalbound = None,
                       trapezoidalbound = None,
                       geant4RegistryAdd = False,
                       flukaConvert = True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaDrift: Making drfit element ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        beampipeMaterialName = element["beampipeMaterial"]
        beampipeRadius       = element["beampipeRadius"]
        beampipeThickness    = element["beampipeThickness"]

        vacuumMaterial = element["vacuumMaterial"]

        e1 = element["outerE1"]
        e2 = element["outerE2"]
        p1 = element['outerP1']
        p2 = element['outerP2']

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make beampipe
        [bpLogical, bpPhysical] = _MakeBeamPipeCircular(g4registry, motherLogical=outerLogical,
                                                        name = name,
                                                        length=length,
                                                        beamPipeRadius=beampipeRadius,
                                                        beamPipeThickness=beampipeThickness,
                                                        beamPipeMaterialName=beampipeMaterialName,
                                                        e1=e1, p1=p1, e2=e2, p2=p2)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "drift")


    def MakeFlukaRBend(self,
                       name,
                       element,
                       rotation = _np.array([[1,0,0],[0,1,0],[0,0,1]]),
                       translation = _np.array([0,0,0]),
                       geomtranslation = _np.array([0,0,0]),
                       cubicalbound = None,
                       trapezoidalbound = None,
                       geant4RegistryAdd = False,
                       flukaConvert = True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaRBend: Making rbend element ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        beampipeMaterialName = element["beampipeMaterial"]
        beampipeRadius       = element["beampipeRadius"]
        beampipeThickness    = element["beampipeThickness"]

        vacuumMaterial = element["vacuumMaterial"]

        e1 = element["outerE1"]
        e2 = element["outerE2"]
        p1 = element['outerP1']
        p2 = element['outerP2']

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make beampipe
        [bpLogical, bpPhysical] = _MakeBeamPipeCircular(g4registry, motherLogical=outerLogical,
                                                        name = name,
                                                        length=length,
                                                        beamPipeRadius=beampipeRadius,
                                                        beamPipeThickness=beampipeThickness,
                                                        beamPipeMaterialName=beampipeMaterialName,
                                                        e1=e1, p1=p1, e2=e2, p2=p2)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "rbend")


    def MakeFlukaSBend(self,
                       name,
                       element,
                       rotation = _np.array([[1,0,0],[0,1,0],[0,0,1]]),
                       translation = _np.array([0,0,0]),
                       geomtranslation = _np.array([0,0,0]),
                       cubicalbound = None,
                       trapezoidalbound = None,
                       geant4RegistryAdd = False,
                       flukaConvert = True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaSBend: Making sbend element ", name)

        length = element.length*1000
        angle = element["angle"]
        chord = 2 * (length / angle) * _np.sin(angle / 2)


        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        beampipeMaterialName = element["beampipeMaterial"]
        beampipeRadius       = element["beampipeRadius"]
        beampipeThickness    = element["beampipeThickness"]

        vacuumMaterial = element["vacuumMaterial"]

        e1 = element["outerE1"]
        e2 = element["outerE2"]
        p1 = element['outerP1']
        p2 = element['outerP2']

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name,
                                                            motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make beampipe
        [bpLogical, bpPhysical] = _MakeBeamPipeCircular(g4registry, motherLogical=outerLogical,
                                                        name = name,
                                                        length=chord,
                                                        beamPipeRadius=beampipeRadius,
                                                        beamPipeThickness=beampipeThickness,
                                                        beamPipeMaterialName=beampipeMaterialName,
                                                        e1=e1, p1=p1, e2=e2, p2=p2)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "sbend")


    def MakeFlukaQuadrupole(self,
                            name,
                            element,
                            rotation=_np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                            translation=_np.array([0, 0, 0]),
                            geomtranslation=_np.array([0, 0, 0]),
                            cubicalbound=None,
                            trapezoidalbound=None,
                            geant4RegistryAdd=False,
                            flukaConvert=True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaQuadrupole: Making quadrupole element ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        beampipeMaterialName = element["beampipeMaterial"]
        beampipeRadius       = element["beampipeRadius"]
        beampipeThickness    = element["beampipeThickness"]

        vacuumMaterial = element["vacuumMaterial"]

        e1 = element["outerE1"]
        e2 = element["outerE2"]
        p1 = element['outerP1']
        p2 = element['outerP2']

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make beampipe
        [bpLogical, bpPhysical] = _MakeBeamPipeCircular(g4registry, motherLogical=outerLogical,
                                                        name = name,
                                                        length=length,
                                                        beamPipeRadius=beampipeRadius,
                                                        beamPipeThickness=beampipeThickness,
                                                        beamPipeMaterialName=beampipeMaterialName,
                                                        e1=e1, p1=p1, e2=e2, p2=p2)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "quad")

    def MakeFlukaTarget(self,
                        name,
                        element,
                        rotation=_np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                        translation=_np.array([0, 0, 0]),
                        geomtranslation=_np.array([0, 0, 0]),
                        cubicalbound=None,
                        trapezoidalbound=None,
                        geant4RegistryAdd=False,
                        flukaConvert=True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaTarget: Making target element ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        targetMaterial = element["material"]
        targetApertureType = element["apertureType"]
        targetHorizontalSize = element["horizontalWidth"]
        targetVerticalSize = element["verticalWidth"]

        e1 = element["outerE1"]
        e2 = element["outerE2"]
        p1 = element['outerP1']
        p2 = element['outerP2']

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make beampipe
        [targetLogical, targetPhysical] = _MakeTarget(g4registry,
                                                      motherLogical=outerLogical,
                                                      name = name,
                                                      apertureType=targetApertureType,
                                                      length=length,
                                                      horizontalWidth=targetHorizontalSize,
                                                      verticalWidth=targetVerticalSize,)


        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "target")

    def MakeFlukaRCol(self,
                      name,
                      element,
                      rotation=_np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                      translation=_np.array([0, 0, 0]),
                      geomtranslation=_np.array([0, 0, 0]),
                      cubicalbound=None,
                      trapezoidalbound=None,
                      geant4RegistryAdd=False,
                      flukaConvert=True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaRCol: Making ecol element ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        horizontalWidth = element['horizontalWidth']
        verticalWidth = element['verticalWidth']
        material = element['material']
        xsize = element['xsize']
        ysize = element['ysize']

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make collimator
        [rcolLogical, rcolPhysical] = _MakeRCol(g4registry, name=name, motherLogical=outerLogical,
                                                length=length,
                                                material=material,
                                                horizontalWidth=horizontalWidth,
                                                verticalWidth=verticalWidth,
                                                xsize=xsize,
                                                ysize=ysize)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "rcol")

    def MakeFlukaECol(self,
                      name,
                      element,
                      rotation=_np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                      translation=_np.array([0, 0, 0]),
                      geomtranslation=_np.array([0, 0, 0]),
                      cubicalbound=None,
                      trapezoidalbound=None,
                      geant4RegistryAdd=False,
                      flukaConvert=True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaECol: Making target ecol ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        horizontalWidth = element['horizontalWidth']
        verticalWidth = element['verticalWidth']
        material = element['material']
        xsize = element['xsize']
        ysize = element['ysize']

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make collimator
        [ecolLogical, ecolPhysical] = _MakeECol(g4registry,
                                                name=name,
                                                motherLogical=outerLogical,
                                                length=length,
                                                material=material,
                                                horizontalWidth=horizontalWidth,
                                                verticalWidth=verticalWidth,
                                                xsize=xsize,
                                                ysize=ysize)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "ecol")

    def MakeFlukaJCol(self,
                      name,
                      element,
                      rotation=_np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                      translation=_np.array([0, 0, 0]),
                      geomtranslation=_np.array([0, 0, 0]),
                      cubicalbound=None,
                      trapezoidalbound=None,
                      geant4RegistryAdd=False,
                      flukaConvert=True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaJCol: Making target jcol ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        xsize = element['xsize']
        ysize = element['ysize']
        xsizeLeft = element['xsizeLeft']
        xsizeRight = element['xsizeRight']
        jawTiltLeft = element['jawTiltLeft']
        jawTiltRight = element['jawTiltRight']
        horizontalWidth = element['horizontalWidth']
        verticalWidth = element['verticalWidth']
        material = element['material']

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make collimator
        [jcolLeftLogical, jcolLeftPhysical], [jcolRightLogical, jcolRightPhysical] \
            = _MakeJCol(g4registry,
                        name=name,
                        motherLogical=outerLogical,
                        length=length,
                        material=material,
                        horizontalWidth=horizontalWidth,
                        verticalWidth=verticalWidth,
                        xsize=xsize,
                        ysize=ysize,
                        xsizeLeft=xsizeLeft,
                        xsizeRight=xsizeRight,
                        jawTiltLeft=jawTiltLeft,
                        jawTiltRight=jawTiltRight)


        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "jcol")


    def MakeFlukaShield(self,
                        name,
                        element,
                        rotation=_np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                        translation=_np.array([0, 0, 0]),
                        geomtranslation=_np.array([0, 0, 0]),
                        cubicalbound=None,
                        trapezoidalbound=None,
                        geant4RegistryAdd=False,
                        flukaConvert=True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaShield: Making target shield ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        beampipeMaterialName = element["beampipeMaterial"]
        beampipeRadius       = element["beampipeRadius"]
        beampipeThickness    = element["beampipeThickness"]

        vacuumMaterial = element["vacuumMaterial"]

        e1 = element["outerE1"]
        e2 = element["outerE2"]
        p1 = element['outerP1']
        p2 = element['outerP2']

        horizontalWidth = element["horizontalWidth"]
        verticalWidth = element["verticalWidth"]
        xsize = element["xsize"]
        ysize = element["ysize"]
        material = element["material"]

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make beampipe
        [bpLogical, bpPhysical] = _MakeBeamPipeCircular(g4registry, motherLogical=outerLogical,
                                                        name = name,
                                                        length=length,
                                                        beamPipeRadius=beampipeRadius,
                                                        beamPipeThickness=beampipeThickness,
                                                        beamPipeMaterialName=beampipeMaterialName,
                                                        e1=e1, p1=p1, e2=e2, p2=p2)

        # make shield
        [shieldLogical, shieldPhysical] = _MakeShield(g4registry,
                                                      name=name,
                                                      motherLogical=outerLogical,
                                                      length=length,
                                                      material=material,
                                                      horizontalWidth=horizontalWidth,
                                                      verticalWidth=verticalWidth,
                                                      xsize=xsize,
                                                      ysize=ysize)


        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "shield")


    def MakeFlukaDump(self,
                      name,
                      element,
                      rotation=_np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                      translation=_np.array([0, 0, 0]),
                      geomtranslation=_np.array([0, 0, 0]),
                      cubicalbound=None,
                      trapezoidalbound=None,
                      geant4RegistryAdd=False,
                      flukaConvert=True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaDump: Making dump ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        # material = element["material"]
        horizontalWidth = element["horizontalWidth"]
        verticalWidth = element["verticalWidth"]
        apertureType = element["apertureType"]

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make dump
        [dumpLogical, dumpPhysical] = _MakeDump(g4registry,
                                                name=name,
                                                motherLogical=outerLogical,
                                                length=length,
                                                material="BLCKHOLE",
                                                horizontalWidth=horizontalWidth,
                                                verticalWidth=verticalWidth,
                                                apertureType=apertureType)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "dump")


    def MakeFlukaWireScanner(self,
                             name,
                             element,
                             rotation=_np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                             translation=_np.array([0, 0, 0]),
                             geomtranslation=_np.array([0, 0, 0]),
                             cubicalbound=None,
                             trapezoidalbound=None,
                             geant4RegistryAdd=False,
                             flukaConvert=True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaWireScanner: Making wirescanner ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        e1 = element["outerE1"]
        e2 = element["outerE2"]
        p1 = element['outerP1']
        p2 = element['outerP2']

        beampipeMaterialName = element["beampipeMaterial"]
        beampipeRadius       = element["beampipeRadius"]
        beampipeThickness    = element["beampipeThickness"]
        vacuumMaterial = element["vacuumMaterial"]

        wireMaterial = element["wireMaterial"]
        wireDiameter = element["wireDiameter"]
        wireLength = element["wireLength"]
        wireAngle = element["wireAngle"]
        wireOffsetX = element["wireOffsetX"]
        wireOffsetY = element["wireOffsetY"]
        wireOffsetZ = element["wireOffsetZ"]

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry,
                                                            name = name,
                                                            motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        # make beampipe
        [bpLogical, bpPhysical] = _MakeBeamPipeCircular(g4registry,
                                                        motherLogical=outerLogical,
                                                        name = name,
                                                        length=length,
                                                        beamPipeRadius=beampipeRadius,
                                                        beamPipeThickness=beampipeThickness,
                                                        beamPipeMaterialName=beampipeMaterialName,
                                                        e1=e1, p1=p1, e2=e2, p2=p2)

        # make wire
        [wireLogical, wirePhysical] = _MakeWireScanner(g4registry,
                                                        name=name,
                                                        motherLogical=bpLogical.daughterVolumes[0].logicalVolume,
                                                        wireMaterial=wireMaterial,
                                                        wireDiameter=wireDiameter,
                                                        wireLength=wireLength,
                                                        wireAngle=wireAngle,
                                                        wireOffsetX=wireOffsetX,
                                                        wireOffsetY=wireOffsetY,
                                                        wireOffsetZ=wireOffsetZ)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "wirescanner")

    def MakeFlukaGap(self,
                     name,
                     element,
                     rotation=_np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                     translation=_np.array([0, 0, 0]),
                     geomtranslation=_np.array([0, 0, 0]),
                     cubicalbound=None,
                     trapezoidalbound=None,
                     geant4RegistryAdd=False,
                     flukaConvert=True):

        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaGap: Making target gap ", name)

        length = element.length*1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,outerLogical, outerPhysical, flukaConvert,
                                                rotation, translation, geomtranslation, "gap")

    def MakeFlukaSampler(self,
                         name,
                         element,
                         rotation = _np.array([[1,0,0],[0,1,0],[0,0,1],[0,0,0]]),
                         translation = _np.array([0,0,0]),
                         geomtranslation = _np.array([0,0,0]),
                         cubicalbound = None,
                         trapezoidalbound = None,
                         geant4RegistryAdd = False,
                         flukaConvert = True,
                         material=None):
        if self.verbose :
            print("pyflubl.BuilderNew.Machine.MakeFlukaSampler: Making sampler element ", name)


        if not material:
            material = self.options.samplerMaterial

        length = element.length*1000
        rotation, geomtranslation = self._MakeOffsetAndTiltTransforms(element, rotation, geomtranslation)
        samplerMaterialName = element["samplerMaterial"]
        samplerDiameter = element["samplerDiameter"]
        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make fake geant4 materials for conversion
        samplerMaterial = _pyg4.geant4.MaterialSingleElement(name=samplerMaterialName, atomic_number=1, atomic_weight=1, density=1)

        # make box of correct size
        samplersolid    = _pyg4.geant4.solid.Box(name+"_solid",samplerDiameter,samplerDiameter,length,g4registry)
        samplerlogical  = _pyg4.geant4.LogicalVolume(samplersolid,samplerMaterial,name+"_lv",g4registry)
        samplerphysical = _pyg4.geant4.PhysicalVolume([0,0,0],
                                                      [0,0,0],
                                                      samplerlogical,
                                                      name+"_pv",
                                                      self.worldLogical,
                                                      g4registry)

        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        return self._MakeFlukaComponentCommonG4(name,samplerlogical, samplerphysical, flukaConvert,
                                                rotation, translation, geomtranslation, "sampler")

    def MakeFlukaCustomG4(self,
                         name,
                         element,
                         rotation = _np.array([[1,0,0],[0,1,0],[0,0,1],[0,0,0]]),
                         translation = _np.array([0,0,0]),
                         geomtranslation = _np.array([0,0,0]),
                         cubicalbound = None,
                         trapezoidalbound = None,
                         geant4RegistryAdd = False,
                         flukaConvert = True,
                         material=None):

        # length
        length = element.length * 1000
        rotation, translation = self._MakeOffsetAndTiltTransforms(element, rotation, translation)

        outerHorizontalSize = element["outerHorizontalSize"]
        outerVerticalSize   = element["outerVerticalSize"]
        outerMaterial       = element["outerMaterial"]

        # registry
        g4registry = self._GetGeant4Registry(geant4RegistryAdd)

        # make outer volume
        [outerLogical, outerPhysical] = _MakeOuterTrapezoid(g4registry, name = name, motherLogical=self.worldLogical,
                                                            tra_coords=trapezoidalbound*1000,
                                                            outerVerticalSize=outerVerticalSize,
                                                            outerMaterial=outerMaterial)


        self._AddBookkeepingTransformation(name, rotation, translation, geomtranslation)

        self._MakeFlukaComponentCommonG4(name, outerLogical, outerPhysical, flukaConvert,
                                         rotation, translation, geomtranslation, "customg4")

    def MakeFlukaCustomFluka(self, name, element,
                             rotation = _np.array([[1,0,0],[0,1,0],[0,0,1],[0,0,0]]),
                             translation = _np.array([0,0,0]),
                             geomtranslation = _np.array([0,0,0]),
                             cubicalbound=None,
                             trapezoidalbound=None,
                             geant4RegistryAdd=False,
                             flukaConvert=True):

        regionNamesTransferred = []

        outer_bodies  = element["customOuterBodies"]
        regions       = element["customRegions"]
        flukaRegistry = element['flukaRegistry']

        if flukaConvert:
            print('MakeFlukaCustomFluka')

            # cut out regions for placement
            for body in outer_bodies:
                z = _pyg4.fluka.Zone()
                z.addIntersection(body)
                self.worldzone.addSubtraction(z)

            # transfer bodies and regions to fluka registry
            for region in regions:
                regionNamesTransferred.append(region.name)

                if region.name not in self.flukaregistry.regionDict :
                    self.flukaregistry.addRegion(region)
                for zone in region.zones :
                    for body in zone.bodies() :
                        if body.name not in self.flukaregistry.bodyDict :
                            body = body._transform(rotation, translation)
                            body._scale(0.1)
                            self.flukaregistry.addBody(body)

            # transfer materials to fluka registry
            # loop over regions, find assignmas, find material
            for region in regions:
                region_name = region.name
                fluka_registry = element['flukaRegistry']

                mat = fluka_registry.assignmas[region.name]
                self._GetFlukaRegistry(True).addMaterialAssignments(mat[0],region.name)

        self._AddBookkeepingTransformation(name, rotation, translation)

        self._MakeFlukaComponentCommonFluka(name, regionNamesTransferred, element.category)

    def _GetGeant4Registry(self,geant4RegistryAdd = False) :
        if geant4RegistryAdd:
            if  self.g4registry :
                g4registry = self.g4registry
            else :
                g4registry = _pyg4.geant4.Registry()
        else:
            g4registry = _pyg4.geant4.Registry()

        return g4registry

    def _GetFlukaRegistry(self, flukaRegistryAdd = False) :
        if flukaRegistryAdd :
            if self.flukaregistry :
                flukaregistry = self.flukaregistry
            else :
                flukaregistry = _pyg4.fluka.FlukaRegistry()
        else :
            flukaregistry = _pyg4.fluka.FlukaRegistry()

        return flukaregistry


    def _MakeOffsetAndTiltTransforms(self, element, rotation, translation):
        offsetX = element["offsetX"]
        offsetY = element["offsetY"]
        tilt    = element["tilt"]

        translation = translation + _np.array([offsetX, offsetY, 0])
        rotation =  rotation @ _tbxyz2matrix([0,0,tilt])

        return rotation, translation

    def _AddBookkeepingTransformation(self, name, rotation, translation, geomtranslation = _np.array([0,0,0]), angle=0.0, k1=0.0):
        self.elementBookkeeping[name]['rotation'] = rotation.tolist()
        self.elementBookkeeping[name]['translation'] = translation.tolist()
        self.elementBookkeeping[name]['geomtranslation'] = geomtranslation.tolist()
        self.elementBookkeeping[name]['angle'] = angle
        self.elementBookkeeping[name]['k1'] = k1

    def _MakeFlukaComponentCommonG4(self, name, containerLV, containerPV, flukaConvert,
                                    rotation, translation, geomtranslation, category,
                                    convertMaterials = False):
        # convert materials
        if convertMaterials:
            print("_MakeFlukaComponentCommon> convertMaterials")
            materialNameSet = containerLV.makeMaterialNameSet()
            self._MakeFlukaMaterials(list(materialNameSet))

        rotation = rotation @ _tbxyz2matrix(containerPV.rotation.eval())

        # convert geometry
        if flukaConvert:
            flukaouterregion, self.flukanamecount = _geant4PhysicalVolume2Fluka(containerPV,
                                                                                mtra=rotation,
                                                                                tra=geomtranslation,
                                                                                flukaRegistry=self.flukaregistry,
                                                                                flukaNameCount=self.flukanamecount,
                                                                                bakeTransforms=self.bakeTransforms)

            # cut volume out of mother zone
            for daughterzones in flukaouterregion.zones:
                self.worldzone.addSubtraction(daughterzones)

        # make bookkeeping information
        if name not in self.elementBookkeeping :
            self.elementBookkeeping[name] = {}

        self.elementBookkeeping[name]['category'] = category

        # needed to book keep potentially deep lv-pv constructions in conversion
        physicalVolumeNames = containerLV.makeLogicalPhysicalNameSets()[1]
        physicalVolumeNames.add(containerPV.name)
        self.elementBookkeeping[name]['physicalVolumes'] = list(physicalVolumeNames)
        try:
            self.elementBookkeeping[name]['flukaRegions'] = [self.flukaregistry.PhysVolToRegionMap[pv] for pv in
                                                             self.elementBookkeeping[name]['physicalVolumes']]
        except KeyError:
            pass

        # make transformed mesh for overlaps
        outerMesh = self._MakePlacedMesh(containerPV, rotation, geomtranslation)
        return {"placedmesh": outerMesh}

    def _MakeFlukaComponentCommonFluka(self, name, regionNames, category) :

        # make bookkeeping information
        if name not in self.elementBookkeeping :
            self.elementBookkeeping[name] = {}

        self.elementBookkeeping[name]['flukaRegions'] = regionNames
        self.elementBookkeeping[name]['category'] = category

    def _MakeGeant4GenericTrap(self, name,
                               length = 500, xhalfwidth = 50, yhalfwidth = 50,
                               e1=0, e2=0,
                               g4registry = None):

        if not g4registry :
            g4registry = self.g4registry

        p1x = -length/2 + yhalfwidth * _np.tan(e1)
        p1y = yhalfwidth
        p2x = -length/2 - yhalfwidth * _np.tan(e1)
        p2y = -yhalfwidth
        p3x =  length/2 - yhalfwidth * _np.tan(e2)
        p3y = -yhalfwidth
        p4x =  length/2 + yhalfwidth * _np.tan(e2)
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

    def _MakePlacedMesh(self, physVol, rotation, translation):

        mesh = physVol.logicalVolume.solid.mesh()

        aa = _tbxyz2axisangle(_matrix2tbxyz(rotation))
        mesh.rotate(aa[0], -aa[1] / _np.pi * 180.0)
        mesh.translate([translation[0], translation[1], translation[2]])

        return mesh

# dynamic doc strings
Machine.AddDrift.__doc__ = """allowed kwargs: """ + \
                           " ".join(_Element._beampipe_allowed_keys) + \
                           " " + " ".join(_Element._outer_allowed_keys)
Machine.AddRBend.__doc__ = """allowed kwargs: """ + \
                           " ".join(_Element._beampipe_allowed_keys) + \
                           " " + " ".join(_Element._outer_allowed_keys) + \
                           " " + " ".join(_Element._rbend_allowed_keys) + \
                           " " + " ".join(_Element._tiltshift_allowed_keys)
Machine.AddSBend.__doc__ = """allowed kwargs: """ + \
                           " ".join(_Element._beampipe_allowed_keys) + \
                           " " + " ".join(_Element._outer_allowed_keys) + \
                           " " + " ".join(_Element._sbend_allowed_keys) + \
                           " " + " ".join(_Element._tiltshift_allowed_keys)
Machine.AddQuadrupole.__doc__ = """allowed kwargs """ + \
                                " ".join(_Element._beampipe_allowed_keys) + \
                                " " + " ".join(_Element._outer_allowed_keys) + \
                                " " + " ".join(_Element._quadrupole_allowed_keys) + \
                                " " + " ".join(_Element._tiltshift_allowed_keys)
Machine.AddTarget.__doc__ = """allowed kwargs""" \
                            " " + " ".join(_Element._outer_allowed_keys) + \
                            " " + " ".join(_Element._tiltshift_allowed_keys) + \
                            " " + " ".join(_Element._target_allowed_keys)
Machine.AddRCol.__doc__ = """allowed kwargs """ + \
                          " " + " ".join(_Element._outer_allowed_keys) + \
                          " " + " ".join(_Element._tiltshift_allowed_keys) + \
                          " " + " ".join(_Element._rcol_allowed_keys)
Machine.AddECol.__doc__ = """allowed kwargs """ + \
                          " " + " ".join(_Element._outer_allowed_keys) + \
                          " " + " ".join(_Element._tiltshift_allowed_keys) + \
                          " " + " ".join(_Element._ecol_allowed_keys)
Machine.AddJCol.__doc__ = """allowed kwargs """ + \
                          " " + " ".join(_Element._outer_allowed_keys) + \
                          " " + " ".join(_Element._tiltshift_allowed_keys) + \
                          " " + " ".join(_Element._jcol_allowed_keys)
Machine.AddShield.__doc__ = """allowed kwargs """ + \
                            " " + " ".join(_Element._outer_allowed_keys) + \
                            " " + " ".join(_Element._tiltshift_allowed_keys) + \
                            " " + " ".join(_Element._beampipe_allowed_keys) + \
                            " " + " ".join(_Element._shield_allowed_keys)
Machine.AddDump.__doc__ = """allowed kwargs """ + \
                          " " + " ".join(_Element._outer_allowed_keys) + \
                          " " + " ".join(_Element._tiltshift_allowed_keys) + \
                          " " + " ".join(_Element._dump_allowed_keys)
Machine.AddWireScanner.__doc__ = """allowed kwargs """ + \
                                 " " + " ".join(_Element._outer_allowed_keys) + \
                                 " " + " ".join(_Element._tiltshift_allowed_keys) + \
                                 " " + " ".join(_Element._beampipe_allowed_keys) + \
                                 " " + " ".join(_Element._wirescanner_allowed_keys)
Machine.AddGap.__doc__ = """allowed kwargs """ + \
                         " " + " ".join(_Element._outer_allowed_keys) + \
                         " " + " ".join(_Element._tiltshift_allowed_keys)

Machine.AddCustomG4.__doc__ = """allowed kwargs """ + \
                              " " + " ".join(_Element._customg4_allowed_keys)
Machine.AddCustomG4File.__doc__ = """allowed kwargs """ + \
                                  " " + " ".join(_Element._customg4file_allowed_keys)
Machine.AddSamplerPlane.__doc__ = """allowed kwargs: """ + \
                                  " ".join(_Element._sampler_plane_allowed_keys)
Machine.AddCustomFluka.__doc__ = """allowed kwargs: """ + \
                                 " ".join(_Element._customfluka_allowed_keys)
Machine.AddCustomFlukaFile.__doc__ = """allowed kwargs: """ + \
                                     " ".join(_Element._customflukafile_allowed_keys)