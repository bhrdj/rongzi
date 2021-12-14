import pandas as pd

forest = pd.read_csv("trees/WikiCCD_2021-07-18_TradOnly.csv")
# Fields: [Component, Strokes, CompositionType, LeftComponent, LeftStrokes, RightComponent, RightStrokes, Signature, Notes, Section]


class CharTree():
    """make it work"""
    def __init__(self, char):
        self._char = char
        self._forestIndex = forest.loc[forest.Component == self.char].index[0]
        self._left = forest.iloc[self.forestIndex].LeftComponent
        self._right = forest.iloc[self.forestIndex].RightComponent
        self._c1 = (i for i in [self.left, self.right] if i != '*')
        self.c2 = []
        self.c3 = []
        self.c4 = []
        self.c6 = []
        self.c7 = []
        self.c8 = []
        self._p1_series = self.findParents(self.char)
        self._p1 = tuple(self._p1_series)

    @staticmethod
    def findParents(char):
        left = forest.loc[forest.LeftComponent == char].Component
        right = forest.loc[forest.RightComponent == char].Component
        return pd.concat([left, right], axis=0)

    @property
    def char(self):
        return self._char

    @property
    def forestIndex(self):
        return self._forestIndex

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def c1(self):
        return self._c1

    @property
    def p1_series(self):
        return self._p1_series

    @property
    def p1(self):
        return self._p1
