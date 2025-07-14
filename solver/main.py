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

    def __repr__(self):
        func = f'Functions:\n  ' + '\n  '.join(f.__repr__() for f in self.functions)
        return func

    def findPossible(self, using) -> list[SolverFunction]:
        candidates = []

        for func in self.functions:
            if func.isCallableWith(using): candidates.append(func)

        return candidates
    
    def tracePath(self, inpt, outp, trace: list = None) -> list[SolverFunction]:

        if trace is None: trace = list()

        paths = self.findPossible(inpt)

        for p in paths:
            if p in trace: continue
            trace.append(p)

            if outp == p.footprint.output: return trace

            m_inpt = (*inpt, p.footprint.output)
            return self.tracePath(m_inpt, outp, trace=trace)

    def solve(self, inpt: dict, outp):
        print(tuple(inpt.keys()))
        path = self.tracePath(tuple(inpt.keys()), outp)

        print(path)

        m_inpt = inpt
        for func in path:
            outp = func(**m_inpt)
            m_inpt = {**m_inpt, **outp}

        return m_inpt

if __name__ == '__main__':

    f_0 = SolverFunction(funclib.add,      Footprint(('x', 'y'), 'z'), {'x': 'x', 'y': 'y'})
    f_1 = SolverFunction(funclib.exponent, Footprint(('x',), 'a'), {'x': 'x'})
    f_2 = SolverFunction(funclib.exponent, Footprint(('y',), 'b'), {'y': 'x'})
    f_3 = SolverFunction(funclib.exponent, Footprint(('z',), 'c'), {'z': 'x'})
    f_4 = SolverFunction(funclib.mul,      Footprint(('a', 'b'), 'c'), {'a': 'x', 'b': 'y'})
    solver = Solver([f_0, f_1, f_2, f_3, f_4])

    r = solver.tracePath(('x', 'y'), 'c')
    print(r)

    r = solver.solve({'x': 3, 'y': 4}, 'c')
    print(r)