import numpy as np

class C_Node:
    def __init__(self, plansza):
        self.znp_stan = np.copy(plansza)
        self.parent = None
        self.children = []
        self.score = 0
        self.color = 0

    def f_dodaj_dziecko(self):
        child = C_Node(self.znp_stan)
        child.parent = self
        self.children.append(child)
        return child
