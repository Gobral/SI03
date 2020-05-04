import numpy as np

class C_Node:
    def __init__(self, plansza):
        self.znp_stan = np.copy(plansza)
        self.parent = None
        self.children = []
        self.score = 0
        self.color = 0
        self.graj = True

    def f_dodaj_dziecko(self):
        child = C_Node(self.znp_stan)
        child.parent = self
        self.children.append(child)
        return child
    
    def f_oblicz_min(self):
        min_w = 1000000
        min_n = None
        for c in self.children:
            if c.score < min_w:
                min_w = c.score
                min_n = c
            elif c.score == min_w and np.random.rand() > 0.5:
                min_w = c.score
                min_n = c
        
        if min_n != None:
            self.score = min_w

        return min_n

    def f_oblicz_max(self):
        max_w = -1000000
        max_n = None
        for c in self.children:
            if c.score > max_w:
                max_w = c.score
                max_n = c
            elif c.score == max_w and np.random.rand() > 0.5:
                max_w = c.score
                max_n = c
        
        if max_n != None:
            self.score = max_w

        return max_n


