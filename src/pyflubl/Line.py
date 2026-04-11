from .Element import Element as _Element
import textwrap as _textwrap

class Line(list) :
    def __init__(self, name, *args):
        self.category = "line"
        for item in args[0]:
            if isinstance(item, _Element):
                raise TypeError("Line is a list of Elements")

        list.__init__(self,*args)
        self.name   = name
        self.length = 0.0
        for item in args[0]:
            self.length += item.length

    def __repr__(self):
        s = ''
        for item in self:
            s += str(item)+'\n' #uses elements __repr__ function
        s += self.name+ ': line=('

        s += ', '.join([item.name for item in self]) + ');'
        s = '\n\t'.join(_textwrap.wrap(s))
        s += "\n"
        return s

    def DefineConstituentElements(self):
        """
        Return a string that contains the lines required
        to define each element in the :class:`Line`.

        Example using predefined Elements name 'd1' and 'q1':

        >>> l = Line([d1,q1])
        >>> f = open("file.txt", "w")
        >>> f.write(l.DefineConsituentElements())
        >>> f.close()
        """
        s = ''
        for item in self:
            s += str(item) #uses elements __repr__ function
        return s