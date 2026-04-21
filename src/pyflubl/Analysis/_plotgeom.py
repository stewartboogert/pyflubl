class PlotgeomDataFile :

    def __init__(self, filename, type="FORMATTED"):
        if type == "FORMATTED":
            self._readFormatted(filename)
        elif type == "UNFORMATTED":
            self._readUnformatterd(filename)

    def _readFormatted(self, filename):
        with open(filename, "rb") as f:
            self.title = f.readline().decode("utf-8").strip()
            f.readline() # "Origin and axis parameters"
            l = f.readline().decode("utf-8").strip().split()
            self.x0pict = float(l[1])
            self.y0pict = float(l[3])
            self.z0pict = float(l[5])
            l = f.readline().decode("utf-8").strip().split()
            self.x1pict = float(l[1])
            self.y1pict = float(l[3])
            self.z1pict = float(l[5])
            l = f.readline().decode("utf-8").strip().split()
            self.tyx = float(l[1])
            self.tyy = float(l[3])
            self.tyz = float(l[5])
            l = f.readline().decode("utf-8").strip().split()
            self.txx = float(l[1])
            self.txy = float(l[3])
            self.txz = float(l[5])
            l = f.readline().decode("utf-8").strip().split()
            self.xaxlen = float(l[1])
            self.yaxlen = float(l[3])

            def readFormattedWorms() :
                pass

    def _readUnformatterd(self, filename):
        # Not yet implemented
        print("Reading unformatted file", filename)
        print("Not yet implemented")
