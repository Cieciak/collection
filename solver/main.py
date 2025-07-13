from types import FunctionType
from collections import namedtuple

import funclib

Footprint = namedtuple('Footprint', ['input', 'output'])


class SolverFunction:

    def __init__(self, function: FunctionType, footprint: Footprint, mapping: dict = None):
        self.__function  = function
        self.__footprint = footprint

        self.__mapping = mapping

    def __repr__(self):
        inpt = ', '.join(self.__footprint.input)
        return f'{self.__function.__name__}({inpt}) -> {self.__footprint.output}'

    def __call__(self, **kwds):
        inpt = {}
        if self.__mapping is not None:
            for key, val in self.__mapping.items():
                inpt[val] = kwds[key]
        else: inpt = kwds

        outp = self.__function(**inpt)

        return {self.__footprint.output: outp}

    @property
    def footprint(self) -> Footprint: return self.__footprint
    
    def isCallableWith(self, known): return all(arg in known for arg in self.footprint.input)


class Solver:

    def __init__(self, functions: list[SolverFunction]):
        self.functions = functions
        self.known = {}

    def __repr__(self):
        func = f'Functions:\n  ' + '\n  '.join(f.__repr__() for f in self.functions)
        vars = f'Variables:\n  ' + '\n  '.join(f'{key}={val}' for key, val in self.known.items())
        return func + '\n' + vars

    def addVariables(self, data: dict):
        self.known = {**self.known, **data}

    def findPossible(self, using) -> list[SolverFunction]:
        candidates = []

        for func in self.functions:
            if func.isCallableWith(using): candidates.append(func)

        return candidates
    
    def tracePath(self, inpt, outp, trace: list = list()):

        paths = self.findPossible(inpt)

        for p in paths:
            if p in trace: continue
            trace.append(p)

            if outp == p.footprint.output: return trace

            m_inpt = (*inpt, p.footprint.output)
            return self.tracePath(m_inpt, outp, trace=trace)



if __name__ == '__main__':

    f_0 = SolverFunction(funclib.areaOfTriangle, Footprint(('x', 'y'), 'z'), {'x': 'base', 'y': 'height'})
    f_1 = SolverFunction(funclib.volume, Footprint(('z', 'y'), 'v'), {'z': 'base', 'y': 'height'})

    solver = Solver([f_0, f_1])
    solver.addVariables({'x': 4, 'y': 3})

    r = solver.tracePath(('x', 'y'), 'v')
    print(r)