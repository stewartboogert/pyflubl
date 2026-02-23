import numpy as _np
import json as _json

from .Builder import Element
from .Builder import Line

def _CalculateElementTransformation(e):
    if e.category == "drift" or  \
            e.category == "quadrupole" or \
            e.category == "target" or \
            e.category == "rcol" or \
            e.category == "ecol" or \
            e.category == "jcol" or \
            e.category == "shield" or \
            e.category == "dump" or \
            e.category == "wirescanner" or \
            e.category == "gap" or \
            e.category == "customG4" or \
            e.category == "customFluka" or \
            e.category == "sampler_plane":

        length = e.length

        rotation = _np.array([[1,0,0],
                              [0,1,0],
                              [0,0,1]])

        rot_sta = rotation
        rot_mid = rotation
        rot_end = rotation

        arc_sta = _np.array([0,0,0])
        arc_end = _np.array([0,0,length])
        arc_mid = arc_end/2.

        cho_sta = arc_sta
        cho_mid = arc_mid
        cho_end = arc_end

        fac_sta = _np.array([0,0,-1])
        fac_end = _np.array([0,0,1])

        return {"rot_sta":rot_sta, "rot_mid":rot_mid, "rot_end":rot_end,
                "arc_sta":arc_sta, "arc_mid":arc_mid, "arc_end":arc_end,
                "cho_sta":cho_sta, "cho_mid":cho_mid, "cho_end":cho_end,
                "fac_sta":fac_sta                   , "fac_end":fac_end}

    elif e.category == "rbend":
        # length is chord length

        a = e['angle']
        l = e.length
        t = 0
        if 'tilt' in e :
            t = e['tilt']

        if abs(a) < 1e-12:
            print("rbend: angle close to zero setting to 1e-12")
            a = 1e-12

        # bending radius
        rho = l/(2*_np.sin(a/2.0))

        tilt = _np.array([[ _np.cos(t), -_np.sin(t), 0],
                          [ _np.sin(t),  _np.cos(t), 0],
                          [ 0         ,           0, 1]])

        rot_sta = _np.array([[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]])
        rot_mid = _np.array([[ _np.cos(a/2), 0, -_np.sin(a/2)],
                             [            0, 1,             0],
                             [ _np.sin(a/2), 0, _np.cos(a/2)]])
        rot_end = _np.array([[ _np.cos(a), 0, -_np.sin(a)],
                             [          0, 1,           0],
                             [ _np.sin(a), 0,  _np.cos(a)]])


        rot_mid = tilt @ rot_mid @ _np.linalg.inv(tilt)
        rot_end = tilt @ rot_end @ _np.linalg.inv(tilt)

        arc_sta = _np.array([0,0,0])
        arc_mid = _np.array([rho*(_np.cos(a/2.) - 1),0,rho*_np.sin(a/2.)])
        arc_end = _np.array([rho*(_np.cos(a) - 1),0,rho*_np.sin(a)])

        cho_sta = _np.array([0,0,0])
        cho_end = l * _np.array([-_np.sin(a/2),0,_np.cos(a/2)])
        cho_mid = cho_end/2.0

        arc_sta = tilt @ arc_sta
        arc_mid = tilt @ arc_mid
        arc_end = tilt @ arc_end

        cho_sta = tilt @ cho_sta
        cho_mid = tilt @ cho_mid
        cho_end = tilt @ cho_end

        fac_sta = _np.array([0,0,-1])
        fac_end = _np.array([0,0,1])

        fac_sta = rot_mid @ fac_sta
        fac_end = rot_mid @ fac_end

        return {"rot_sta":rot_sta, "rot_mid":rot_mid, "rot_end":rot_end,
                "arc_sta":arc_sta, "arc_mid":arc_mid, "arc_end":arc_end,
                "cho_sta":cho_sta, "cho_mid":cho_mid, "cho_end":cho_end,
                "fac_sta":fac_sta                   , "fac_end": fac_end}

    elif e.category == "sbend":
        # length is qrc length

        a = e['angle']
        l = e.length
        t = 0

        if 'tilt' in e:
            t = e['tilt']

        if abs(a) < 1e-12:
            print("sbend: angle close to zero setting to 1e-12")
            a = 1e-12

        # bending radius
        rho = l/a

        tilt = _np.array([[_np.cos(t), -_np.sin(t), 0],
                          [_np.sin(t), _np.cos(t), 0],
                          [0, 0, 1]])

        rot_sta = _np.array([[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]])
        rot_mid = _np.array([[ _np.cos(a/2), 0, -_np.sin(a/2)],
                             [          0, 1,          0],
                             [_np.sin(a/2), 0, _np.cos(a/2)]])
        rot_end = _np.array([[ _np.cos(a), 0, -_np.sin(a)],
                             [          0, 1,          0],
                             [_np.sin(a), 0, _np.cos(a)]])

        rot_sta = tilt @ rot_sta @ _np.linalg.inv(tilt)
        rot_mid = tilt @ rot_mid @ _np.linalg.inv(tilt)
        rot_end = tilt @ rot_end @ _np.linalg.inv(tilt)

        arc_sta = _np.array([0,0,0])
        arc_mid = _np.array([rho*(_np.cos(a/2) - 1),0,rho*_np.sin(a/2)])
        arc_end = _np.array([rho*(_np.cos(a) - 1),0,rho*_np.sin(a)])

        cho_sta = _np.array([0,0,0])
        cho_end = 2*(l/a)*_np.sin(a/2) * _np.array([-_np.sin(a/2),0,_np.cos(a/2)])
        cho_mid = cho_end/2.0

        arc_sta = tilt @ arc_sta
        arc_mid = tilt @ arc_mid
        arc_end = tilt @ arc_end

        cho_sta = tilt @ cho_sta
        cho_mid = tilt @ cho_mid
        cho_end = tilt @ cho_end

        fac_sta = _np.array([0,0,-1])
        fac_end = _np.array([0,0,1])

        fac_sta = rot_sta @ fac_sta
        fac_end = rot_end @ fac_end

        return {"rot_sta":rot_sta, "rot_mid":rot_mid, "rot_end":rot_end,
                "arc_sta":arc_sta, "arc_mid":arc_mid, "arc_end":arc_end,
                "cho_sta":cho_sta, "cho_mid":cho_mid, "cho_end":cho_end,
                "fac_sta":fac_sta                   , "fac_end":fac_end}


class Coordinates(object) :

    def __init__(self):

        self.sequence = []
        self.elements = {}

        self.element_name = []
        self.element_category = []
        self.element_length = []
        self.element_theta = []
        self.element_psi   = []

        self.len_sta = []
        self.len_mid = []
        self.len_end = []

        self.rot_sta = []
        self.rot_mid = []
        self.rot_end = []

        self.arc_sta = []
        self.arc_mid = []
        self.arc_end = []

        self.cho_sta = []
        self.cho_mid = []
        self.cho_end = []

        self.rot_sta = []
        self.rot_mid = []
        self.rot_end = []

        self.fac_sta = []
        self.fac_end = []

    def Append(self, item, addToSequence=True):
        if not isinstance(item, (Element, Line)):
            msg = "Only Elements or Lines can be added to the machine"
            raise TypeError(msg)
        elif item.name not in list(self.elements.keys()):
            #hasn't been used before - define it
            if type(item) is Line:
                for element in item:
                    self.Append(item)
            else:
                self.elements[item.name] = item
        else:
            if self.verbose:
                print("Element of name: ",item.name," already defined, simply adding to sequence")

        # add to the sequence - optional as we may be appending a parent definition to the list
        # of objects to write before the main definitions.
        if addToSequence:
            self.sequence.append(item.name)

    def __len__(self):
        return len(self.element_name)

    def Build(self, circular = False):

        for element_name in self.elements :
            e = self.elements[element_name]
            t = _CalculateElementTransformation(e)

            # name
            self.element_name.append(e.name)

            # length
            self.element_length.append(e.length)

            # category
            self.element_category.append(e.category)

            # bending angle
            try :
                self.element_theta.append(e['angle'])
            except KeyError :
                self.element_theta.append(0)

            # tilt angle
            try :
                self.element_psi.append(e['tilt'])
            except KeyError :
                self.element_psi.append(0)

            if len(self.rot_sta) == 0:
                self.len_sta.append(0)
                self.len_mid.append(e.length/2.0)
                self.len_end.append(e.length)
                self.rot_sta.append(t['rot_sta'])
                self.rot_mid.append(t['rot_mid'])
                self.rot_end.append(t['rot_end'])
                self.arc_sta.append(t['arc_sta'])
                self.arc_mid.append(t['arc_mid'])
                self.arc_end.append(t['arc_end'])
                self.cho_sta.append(t['cho_sta'])
                self.cho_mid.append(t['cho_mid'])
                self.cho_end.append(t['cho_end'])
                self.fac_sta.append(t['fac_sta'])
                self.fac_end.append(t['fac_end'])
            else:
                # get last element variables
                len_end = self.len_end[-1]
                rot_end = self.rot_end[-1]
                arc_end = self.arc_end[-1]

                self.len_sta.append(len_end + 0)
                self.len_mid.append(len_end + e.length/2.0)
                self.len_end.append(len_end + e.length)

                self.rot_sta.append(t['rot_sta'] @ rot_end)
                self.rot_mid.append(t['rot_mid'] @ rot_end)
                self.rot_end.append(t['rot_end'] @ rot_end)

                self.arc_sta.append(rot_end @ t['arc_sta'] + arc_end)
                self.arc_mid.append(rot_end @ t['arc_mid'] + arc_end)
                self.arc_end.append(rot_end @ t['arc_end'] + arc_end)
                self.cho_sta.append(rot_end @ t['cho_sta'] + arc_end)
                self.cho_mid.append(rot_end @ t['cho_mid'] + arc_end)
                self.cho_end.append(rot_end @ t['cho_end'] + arc_end)

                self.fac_sta.append(rot_end @ t['fac_sta'])
                self.fac_end.append(rot_end @ t['fac_end'])

        self._CheckPoleFaces()

    def _CheckPoleFaces(self, circular = False):
        for i, element_name in enumerate(self.elements) :

            # current and next element indices
            i1 = i
            if i < len(self)-1 :
                i2 = i+1
            else :
                if circular :
                    i2 = 0
                else :
                    continue

            # drift/rbend
            if self.element_category[i1] == "drift" and self.element_category[i2] == "rbend" :
                self.fac_end[i1] = - self.fac_sta[i2]
            # rbend/drift
            if self.element_category[i1] == "rbend" and self.element_category[i2] == "drift" :
                self.fac_sta[i2] = - self.fac_end[i1]


    def SaveJSON(self, file_name, indent = 0):
        dict_to_save = {}

        dict_to_save['element_name'] = self.element_name
        dict_to_save['element_category'] = self.element_category
        dict_to_save['element_length'] = self.element_length
        dict_to_save['element_theta'] = self.element_theta
        dict_to_save['element_psi'] = self.element_psi

        dict_to_save['len_sta'] = self.len_sta
        dict_to_save['len_mid'] = self.len_mid
        dict_to_save['len_end'] = self.len_end

        dict_to_save['rot_sta'] = _np.array(self.rot_sta).tolist()
        dict_to_save['rot_mid'] = _np.array(self.rot_mid).tolist()
        dict_to_save['rot_end'] = _np.array(self.rot_end).tolist()

        dict_to_save['arc_sta'] = _np.array(self.arc_sta).tolist()
        dict_to_save['arc_mid'] = _np.array(self.arc_mid).tolist()
        dict_to_save['arc_end'] = _np.array(self.arc_end).tolist()

        dict_to_save['cho_sta'] = _np.array(self.cho_sta).tolist()
        dict_to_save['cho_mid'] = _np.array(self.cho_mid).tolist()
        dict_to_save['cho_end'] = _np.array(self.cho_end).tolist()

        dict_to_save['fac_sta'] = _np.array(self.fac_sta).tolist()
        dict_to_save['fac_end'] = _np.array(self.fac_end).tolist()

        # Pretty-printed
        with open(file_name, "w") as f:
            if indent > 0 :
                _json.dump(dict_to_save, f, indent=indent)
            else :
                _json.dump(dict_to_save, f)

    def LoadJSON(self, file_name):
        with open(file_name, "r") as f:
            data = _json.load(f)

            self.element_name = data['element_name']
            self.element_category = data['element_category']
            self.element_length = data['element_length']
            self.element_theta = data['element_theta']
            self.element_psi = data['element_psi']

            self.len_sta = data['len_sta']
            self.len_mid = data['len_mid']
            self.len_end = data['len_end']

            # make list elements arrays
            self.rot_sta = [_np.array(e) for e in data['rot_sta']]
            self.rot_mid = [_np.array(e) for e in data['rot_mid']]
            self.rot_end = [_np.array(e) for e in data['rot_end']]

            self.arc_sta = [_np.array(e) for e in data['arc_sta']]
            self.arc_mid = [_np.array(e) for e in data['arc_mid']]
            self.arc_end = [_np.array(e) for e in data['arc_end']]

            self.cho_sta = [_np.array(e) for e in data['cho_sta']]
            self.cho_mid = [_np.array(e) for e in data['cho_mid']]
            self.cho_end = [_np.array(e) for e in data['cho_end']]

            self.fac_sta = [_np.array(e) for e in data['fac_sta']]
            self.fac_end = [_np.array(e) for e in data['fac_end']]

    def PandasDataFrame(self):
        import pandas as pd
        df = pd.DataFrame()
        df['element_name'] = self.element_name
        df['element_category'] = self.element_category
        df['element_length'] = self.element_length
        df['element_theta'] = self.element_theta
        df['element_psi'] = self.element_psi

        df['len_sta'] = self.len_sta
        df['len_mid'] = self.len_mid
        df['len_end'] = self.len_end

        df['rot_sta'] = self.rot_sta
        df['rot_mid'] = self.rot_mid
        df['rot_end'] = self.rot_end

        df['arc_sta'] = self.arc_sta
        df['arc_mid'] = self.arc_mid
        df['arc_end'] = self.arc_end

        df['cho_sta'] = self.cho_sta
        df['cho_mid'] = self.cho_mid
        df['cho_end'] = self.cho_end

        df['fac_sta'] = self.fac_sta
        df['fac_end'] = self.fac_end

        return df