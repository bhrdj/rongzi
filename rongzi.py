#!/usr/bin/env python3

import pandas as pd, numpy as np, pickle, graphviz
#!conda install pandas=1.3.4

class RongZi(object):
    """
        Supply Chinese characters, 
        and the application will find optimized paths connecting them,
        via a chain of component-neighbor-relationships.
    """
            
    def __init__(self, c:str='蓉', *args, **kwargs):
        self.component = c
        self.neighbors = {c}
        self.paths = {c: [c]}
        self.scores = {c: 0}        
        
    def _load_class_objects() -> tuple[pd.DataFrame, dict, dict]:
        """
            LOAD ccd, pdb, & kdb DICTIONARIES AS CLASS OBJECTS:
            ccd:
                pd.DataFrame Chinese Character Decomposition
                indices are components, values are characteristics of component.
            pdb:
                dict[str, str] Parents Database
                keys are components, values are parent-/decomposed-components.
            kdb:
                dict[str, str] Kids Database
                keys are components, values are child-/composite-components.
        """
        with open('./assets/ccd_pdb_kdb.pickle', 'rb') as f:
            ccd, pdb, kdb = pickle.load(f)
        del f
        return ccd, pdb, kdb

    # GRANULAR METHODS FOR WALKING THE GRAPH OF NEIGHBOR COMPONENTS
    @classmethod
    def get_kids(self, c:str) -> list[str]:
        """
        Components may have any number of kids.
        Kids are formed by composition of a component with another component.
        """
        return self.kdb[c]
    
    @classmethod
    def get_parents(self, c:str) -> list[str]:
        """
        Components initially have a maximum of two parents. 
        Up to a max of ~6 after string split.
        Parents are formed by decomposition of a component into sub-components.
        """
        l = self.pdb[c]
        l = [list(i) for i in l if i]
        l = [item for sublist in l for item in sublist 
             if item not in ['?', '*', c, 'nan']]
        try:
            l.remove(c)
        except ValueError:
            pass
        return l
    
    # METHODS TO SCORE AND SORT PATHS
    @staticmethod
    def scorefunc(strokes:int):
        """For some stroke-count, calculate the increase in a path's score."""
        x = strokes - 6
        y1 = 0 if x < 0 else .001*x**2
        y2 = 0 if x > 0 else .07*np.exp(-x)
        return 1 + y1 + y2
    
    @classmethod
    def score(self, c:str) -> int:
        """For a component, get stroke-count & return the path-score increase."""
        strokes = self.ccd.loc[c].Strokes
        epsilon = 0.1 / ord(c)
        return self.scorefunc(strokes) + epsilon

    # METHODS TO GROW NEIGHBORHOOD
    def _add_neighbor_path_and_score(self, previous:str, new:str):
        """Internal method to add a character component to an instance."""
        self.neighbors.add(new)
        self.paths[new] = self.paths[previous] + [new]
        self.scores[new] = self.scores[previous] + self.score(new)
    
    def add_neighbors(self):
        """Grow the instance's neighborhood by 1 character in all directions."""
        neighbors, scores = self.neighbors.copy(), self.scores.copy()
        for i in neighbors:
            newfolk = self.get_parents(i) + self.get_kids(i)
            for j in newfolk:
                if j is None:
                    continue
                # Add path if the neighbor-component is new,
                # replace an old neighbor's path if new path scores better/lower.
                if (
                    (j not in self.neighbors) 
                    or 
                    (self.scores[j] > self.scores[i] + self.score(j))
                ): 
                    self._add_neighbor_path_and_score(i, j)
    
    @classmethod
    def paths_a2b(self, a: 'RongZi', b: 'RongZi', max_paths=5) -> pd.DataFrame:
        """Find paths between components a and b, and sort by path scores."""
        # get the components in the intersection of two neighborhoods
        intersection = a.neighbors.intersection(b.neighbors)
        
        # sum the path scores from each neighborhood's portion, 
        # minus redundant midpoint
        scores = {c: a.scores[c] + b.scores[c] - self.score(c) 
                  for c in intersection}
        scores = pd.Series(scores, name='score').to_frame()
        
        # concat the path scores from each neighborhood's portion, 
        # truncate redundant midpoint
        paths = {c: a.paths[c] + b.paths[c][:-1][::-1] for c in intersection}                
        # convert paths from lists to strings
        paths = {c: ''.join(paths[c]) for c in paths}
        paths = pd.Series(paths, name='path').to_frame()
        
        # drop paths with redundant cycles
        no_redundant_cycles = paths.applymap(lambda x: len(x) == len(set(x)))
        paths = paths[no_redundant_cycles]
        
        # join scores and paths
        paths_scores = paths.join(scores).sort_values('score', ascending=True)
        paths_scores.drop_duplicates(subset='path', inplace=True)  # unnecessary?
        paths_scores.dropna(inplace=True)
                
        return paths_scores.iloc[:max_paths]
    
    @classmethod
    def analyze_sequence(self, 
        seq:str, return_instances=False, **kwargs) -> pd.DataFrame:
        """
            With a sequence of components as a string, 
            get the best paths between each adjacent pair.
        """
        rz = {}
        # initialize and grow instances
        for c in seq:
            rz[c] = RongZi(c)
            while len(rz[c].neighbors) < 1000:
                rz[c].add_neighbors()
        
        # get paths for each adjacent character pair in the input string
        paths = pd.DataFrame()
        for a,b in zip(seq[:-1], seq[1:]):
            paths[a+b] = self.paths_a2b(rz[a],rz[b]).reset_index().iloc[:10].path
        
        if return_instances:
            return paths, rz
        
        return paths        
    
    
#     def get_all_descendants(self):
#     """
#         Populates self.vert_tree with all kids of kids.
#         For each generation, maximum of 10 
#     """
#     c = self.component
#     ad_stack = [c]
#     ad_dict = {}

#     while ad_stack:
#         c = ad_stack.pop(0)
#         kids = self.kdb[c]
#         for kid in kids:
#             if c in 
#             ad_stack.append(kid)
#             ad_list.append(kid)

# #     return ad_list
    
    def get_vertical_family_tree(self, max_sibs=10) -> bool:
        self.vert_tree = graphviz.Digraph(comment='vertical family tree')
        c = self.component
        
        excess_kids = []
        clus = {}
        # get nodes and edges of kids
        kids = self.get_kids(c)
        if len(kids) > max_sibs:
            kids = kids[:max_sibs]
            excess_kids.append(c)
        with self.vert_tree.subgraph(name=str(1)) as clus:
            for k in kids:
                if k == c or k is None:
                    continue
                clus.node(k)
                self.vert_tree.edges([f"{c}{k}"])
        #
        # get nodes and edges of parents
        with self.vert_tree.subgraph(name=str(2)) as clus:
            for p in self.get_parents(c):
                if p is None:
                    continue
                clus.node(p)
                self.vert_tree.edges([f"{p}{c}"])

        self.vert_tree.engine = 'neato'
        self.vert_tree.attr('graph', overlap='false')
        
        return excess_kids
    
    ccd, pdb, kdb = _load_class_objects()


