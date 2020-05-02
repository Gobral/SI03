import numpy as np
from c_node import C_Node

class C_Bot:
    def __init__(self, plansza, kolor):
        self.znp_plansza = plansza
        self.zi_kolor = kolor

        self.f_wykonaj_ruch()

    def f_wykonaj_ruch(self):
        plansza = np.copy(self.znp_plansza)
        if np.sum(plansza) == 0:
            self.znp_plansza[5][3] = self.zi_kolor
            return
        

        