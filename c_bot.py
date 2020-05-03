import numpy as np
from c_node import C_Node

class C_Bot:
    def __init__(self, plansza, kolor, glebokosc):
        self.znp_plansza = plansza
        self.zi_kolor = kolor
        self.zi_glebokosc = glebokosc

    def f_wykonaj_ruch(self):
        if np.sum(self.znp_plansza) == 0:
            self.znp_plansza[5][3] = self.zi_kolor
            return
        
        root = C_Node(self.znp_plansza)
        aktualny = root
        akt_kolor = self.zi_kolor
        ruchy = self.f_generuj_ruchy(aktualny.znp_stan, akt_kolor)
        liscie = []
        for ruch in ruchy:
            l = aktualny.f_dodaj_dziecko()
            l.color = akt_kolor
            l.znp_stan[ruch[0]][ruch[1]] = ruch[2]
            self.f_ocen_node(l)
            print(l.znp_stan)
            print(l.score)

            liscie.append(l)


        licznik = 1
        while licznik <= self.zi_glebokosc:
            if akt_kolor == 1:
                akt_kolor = 2
            else:
                akt_kolor = 1
            nowe_liscie = []
            #for l in liscie:

            licznik += 1 

    def f_generuj_ruchy(self, stan, kolor):
        ret_ruchy = []
        for kol in range(0, len(stan[0])):
            w = len(stan) -1
            while w >= 0:
                if stan[w][kol] == 0:
                    ret_ruchy.append([w, kol, kolor])
                    break
                w -= 1
        
        return ret_ruchy

    def f_ocen_node(self, node):
        ocena = 0
        for kol in node.znp_stan.T:
            i = len(kol) -1
            licznik = 0
            while i >= 0:
                if kol[i] == node.color:
                    licznik += 1
                elif kol[i] != 0:
                    licznik = 0
                else:
                    break
                i -= 1
            if licznik > ocena:
                ocena = licznik

        for kol in range(0, len(node.znp_stan[0]) - 3):
            i = len(node.znp_stan)
        node.score = ocena

        