#!/usr/bin/env python3

import pandas as pd, numpy as np
import graphviz, pickle, gc
#!conda install pandas=1.3.4

class RongZi(object):
    """
        "Melt" a Chinese character
        into neighbors sharing similar components.        
    """
    
    # Load ccd, pdb & kdb dictionaries, as class objects.
        # ccd: pd.DataFrame Chinese Character Decomposition
            # indices are components, values are characteristics of component.
        # pdb: dict[str, str] Parents Database
            # keys are components, values are parent-/decomposed-components.
        # kdb: dict[str, str] Kids Database
            # keys are components, values are child-/composite-components.
    with open('../docs/pickle/ccd_kdb.pickle', 'rb') as f:
        ccd, pdb, kdb = pickle.load(f)
    del f
    
    def __init__(self, component:str, *args, **kwargs):
        self.component = component
        self.neighbors = {component}
        self.paths = {component: [component]}
        self.scores = {component: 0}        
    
    @classmethod
    def get_kids(self, c:str) -> list[str]:
        return self.kdb[c]
    
    @classmethod
    def get_parents(self, c:str) -> list[str]:
        return self.pdb[c]
    
    @staticmethod
    def scorefunc(strokes:int):
        x = strokes - 6
        y1 = 0 if x < 0 else .001*x**2
        y2 = 0 if x > 0 else .07*np.exp(-x)
        return 1 + y1 + y2
    
    @classmethod
    def score(self, c:str) -> int:
        strokes = self.ccd.loc[c].Strokes
        epsilon = 0.1 / ord(c)
        return self.scorefunc(strokes) + epsilon
    
    def _add_neighbor_path_and_score(self, previous:str, new:str):
        self.neighbors.add(new)
        self.paths[new] = self.paths[previous] + [new]
        self.scores[new] = self.scores[previous] + self.score(new)        
    
    def add_neighbors(self):
        neighbors, scores = self.neighbors.copy(), self.scores.copy()
        for i in neighbors:
            newfolk = self.get_parents(i) + self.get_kids(i)
            for j in newfolk:
                if j is None:
                    continue
                if j not in self.neighbors or self.scores[j] > self.score(j):
                    self._add_neighbor_path_and_score(i, j)
    
    @classmethod
    def paths_a2b(self, a: 'RongZi', b: 'RongZi') -> pd.DataFrame:
        # get the components in the intersection of two neighborhoods
        intersection = a.neighbors.intersection(b.neighbors)
        
        # sum the path scores from each neighborhood's portion, minus redundant midpoint
        scores = {c: a.scores[c] + b.scores[c] - self.score(c) for c in intersection}
        scores = pd.Series(scores, name='score').to_frame()
        
        # 
        paths = {c: a.paths[c] + b.paths[c][:-1][::-1] for c in intersection}
        paths = pd.Series(paths, name='path').to_frame()
        
        paths_scores = paths.join(scores).sort_values('score', ascending=True)
        paths_scores['path_str'] = paths_scores.path.map(lambda x: ''.join(x))
        paths_scores.drop_duplicates(subset='path_str', inplace=True)
        paths_scores.drop(columns='path', inplace=True)
        
        return paths_scores
    
    @classmethod
    def analyze_sequence(self, seq:str, return_instances=False) -> pd.DataFrame:
        rz = {}
        for c in seq:
            rz[c] = RongZi(c)
            while len(rz[c].neighbors) < 1000:
                rz[c].add_neighbors()                
        
        paths = pd.DataFrame()
        for a,b in zip(seq[:-1], seq[1:]):
            paths[a+b] = self.paths_a2b(rz[a],rz[b]).reset_index().iloc[:5].path_str
        
        if return_instances:
            return paths, rz
        
        return paths

#     @property
#     def char(self):
