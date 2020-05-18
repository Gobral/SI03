import numpy as np
from c_node import C_Node
import time

class C_Bot:
    def __init__(self, plansza, kolor, glebokosc):
        self.zt_aktualny_czas = time.time()
        self.znp_plansza = plansza
        self.zi_kolor = kolor
        self.kolor_p = 2 if self.zi_kolor == 1 else 1
        self.zi_glebokosc = glebokosc
        self.win_state = 4

    def f_wyswietl_pomiar(self, label):
        zt_nowy = time.time()
        delta = zt_nowy - self.zt_aktualny_czas
        #print(label, "   ", delta)
        self.zt_aktualny_czas = zt_nowy
        return delta

    def f_wykonaj_ruch(self, plansza):
        self.znp_plansza = plansza
        self.f_wyswietl_pomiar("Start sprawdzaia")

        if np.sum(self.znp_plansza) == 0:
            self.znp_plansza[5][np.random.randint(0, 7)] = self.zi_kolor
            delta = self.f_wyswietl_pomiar("Koniec")
            return [self.znp_plansza, True, delta]
        
        root = C_Node(self.znp_plansza)
        root.color = self.zi_kolor

        wyb = self.f_test_alfabeta(root)
        if wyb == root:
            temp = np.random.randint(0, len(root.children) )
            wyb = root.children[temp]
        while(wyb.parent != root):
            wyb = wyb.parent
        self.f_ocen_node(wyb, 1)

        if wyb.score >= self.win_state:
            wyb.graj = False
        self.f_ocen_node(wyb, 2)

        if wyb.score >= self.win_state:
            wyb.graj = False
            
        delta = self.f_wyswietl_pomiar("Koniec")

        return [wyb.znp_stan, wyb.graj, delta]

    def f_test_alfabeta(self, root):
        #alfa = [-1000, None]
        #beta = [1000, None]
        alfa = -1000
        beta = 1000
        kolor_p = 2 if self.zi_kolor == 1 else 1
        #return self.f_minmax_alfa(self.zi_kolor, root, 0, alfa, beta)
        return self.f_test_minmax(kolor_p, root, 0, alfa, beta)

    def f_test_minmax(self, kolor, node, poziom, al, be):
        alfa = al
        beta =be
        kolor_p = 2 if kolor == 1 else 1
        #print(poziom)
        self.f_ocen_node(node, kolor)
        if node.score >= self.win_state:
            temp = self.zi_glebokosc + 3 - poziom
            node.score = node.score * temp
            if kolor != self.zi_kolor:
                node.score = -node.score
            return node
        
        if poziom > self.zi_glebokosc:
            self.f_test_heurystyki(node)
            return node
        
        node.score = -1000
        ruchy = self.f_generuj_ruchy(node.znp_stan, kolor_p)
        #wyniki = []
        

        if kolor != self.zi_kolor:
            maxev = -1000
            maxnode = None
            for ruch in ruchy:
                nl = node.f_dodaj_dziecko()
                nl.color = kolor_p
                nl.znp_stan[ruch[0]][ruch[1]] = ruch[2]
                #wyniki.append(self.f_test_rekurencji(kolor_p, nl, poziom + 1))
                eva = self.f_test_minmax(kolor_p, nl, poziom + 1, alfa, beta)
                if eva.score > maxev:
                    maxev = eva.score
                    maxnode = eva
                

                alfa = max(alfa, eva.score)
                if beta <= alfa:
                    break
            if maxnode != None:
                return maxnode
            else:
                #node.score = 1000
                return node
        else:
            minev = 1000
            minnode = None
            for ruch in ruchy:
                nl = node.f_dodaj_dziecko()
                nl.color = kolor_p
                nl.znp_stan[ruch[0]][ruch[1]] = ruch[2]
                #wyniki.append(self.f_test_rekurencji(kolor_p, nl, poziom + 1))
                eva = self.f_test_minmax(kolor_p, nl, poziom + 1, alfa, beta)
                if eva.score < minev:
                    minev = eva.score
                    minnode = eva

                beta = min(beta, eva.score)
                if beta <= alfa:
                    break
            if minnode != None:
                return minnode
            else:
                #node.score = -1000
                return node

    
    def f_test_generowania(self, root):
        kolor_p = 2 if self.zi_kolor == 1 else 1
        return self.f_test_rekurencji(kolor_p, root, 0)

    def f_test_rekurencji(self, kolor, node, poziom):
        #print(poziom)
        self.f_ocen_node(node, kolor)
        if node.score >= self.win_state:
            temp = self.zi_glebokosc - poziom + 3
            node.score = node.score * temp
            if kolor != self.zi_kolor:
                node.score = -node.score
            return node
        
        if poziom > self.zi_glebokosc:
            self.f_test_heurystyki(node)
            return node

        kolor_p = 2 if kolor == 1 else 1
        node.score = -1000
        ruchy = self.f_generuj_ruchy(node.znp_stan, kolor_p)
        #wyniki = []
        

        for ruch in ruchy:
            nl = node.f_dodaj_dziecko()
            nl.color = kolor_p
            nl.znp_stan[ruch[0]][ruch[1]] = ruch[2]
            #wyniki.append(self.f_test_rekurencji(kolor_p, nl, poziom + 1))
            self.f_test_rekurencji(kolor_p, nl, poziom + 1)

        if kolor != self.zi_kolor:
            return node.f_oblicz_max()
        else:
            return node.f_oblicz_min()
            

    def f_test_heurystyki(self, node):
        temp_ocena = node.score
        
        if node.color != self.zi_kolor:
            self.f_ocen_node(node, self.zi_kolor)
            node.score = node.score - temp_ocena
        else:
            self.f_ocen_node(node, self.kolor_p)
            node.score = temp_ocena - node.score


    def f_generuj_poziom(self, max, root):
        liscie = [root]
        poziom = 0
        while poziom <= max:
            nowe_liscie = []
            for l in liscie:
                nowe_liscie.extend(l.children)
            poziom += 1
            liscie = nowe_liscie

        return liscie

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
    
    def f_ocen_node(self, node, kolor):
        ocena = 0
        temp_kolor = node.color
        node.color = kolor
        for kol in node.znp_stan.T:
            i = len(kol) -1
            licznik = 0
            while i >= 0:
                if kol[i] == node.color:
                    licznik += 1
                elif kol[i] != 0:
                    if licznik >= self.win_state:
                        ocena = licznik
                    licznik = 0
                else:
                    break
                i -= 1
            if licznik > ocena:
                ocena = licznik

        for wier in node.znp_stan:
            if np.sum(wier) != 0:
                licznik = 0
                zera = 0
                for k in wier:
                    if k == node.color:
                        licznik += 1
                    elif k != 0:
                        if zera > 0 and licznik > 0 and licznik > ocena:
                            ocena = licznik
                        if licznik >= self.win_state:
                            ocena = licznik
                        licznik = 0
                        zera = 0
                    else:
                        if licznik > ocena:
                            ocena = licznik
                        licznik = 0
                        zera += 1
                if licznik > ocena:
                    ocena = licznik

        # przeszukiwanie od dołu na ukos w prawo
        for kol in range(0, len(node.znp_stan[0]) - 3):
            i = len(node.znp_stan) - 1
            j = kol 
            zera = 0
            licznik = 0
            while j < len(node.znp_stan[0]) and i >= 0:
                if node.znp_stan[i][j] == node.color:
                    licznik += 1
                elif node.znp_stan[i][j] != 0:
                    if zera > 0 and licznik > 0 and licznik > ocena:
                        ocena = licznik
                    if licznik >= self.win_state:
                        ocena = licznik
                    licznik = 0
                    zera = 0
                else:
                    if licznik > ocena:
                        ocena = licznik
                    licznik = 0
                    zera += 1
        
                j += 1
                i -= 1

            if licznik > ocena:
                ocena = licznik
        
        # przeszukiwanie od dołu na ukos w lewo
        for kol in range(3, len(node.znp_stan[0])):
            i = len(node.znp_stan) - 1
            j = kol 
            
            zera = 0
            licznik = 0
            while j >= 0 and i >= 0:
                if node.znp_stan[i][j] == node.color:
                    licznik += 1
                elif node.znp_stan[i][j] != 0:
                    if zera > 0 and licznik > 0 and licznik > ocena:
                        ocena = licznik
                    if licznik >= self.win_state:
                        ocena = licznik
                    licznik = 0
                    zera = 0
                else:
                    if licznik > ocena:
                        ocena = licznik
                    licznik = 0
                    zera += 1

                j -= 1
                i -= 1

            if licznik > ocena:
                ocena = licznik

        # przeszukiwanie na ukos w prawo pozostale
        for wier in range(len(node.znp_stan) - 3, len(node.znp_stan) - 1):
            if wier > 0:
                i = wier
                j = 0
                zera = 0
                licznik = 0
                while j < len(node.znp_stan[0]) and i >= 0:
                    if node.znp_stan[i][j] == node.color:
                        licznik += 1
                    elif node.znp_stan[i][j] != 0:
                        if zera > 0 and licznik > 0 and licznik > ocena:
                            ocena = licznik
                        if licznik >= self.win_state:
                            ocena = licznik
                        licznik = 0
                        zera = 0
                    else:
                        if licznik > ocena:
                            ocena = licznik
                        licznik = 0
                        zera += 1

                    j += 1
                    i -= 1

                if licznik > ocena:
                    ocena = licznik
        
        # przeszukiwanie na ukos w lewo pozostale
        for wier in range(len(node.znp_stan) - 3, len(node.znp_stan) - 1):
            if wier > 0:
                i = wier
                j = len(node.znp_stan[0]) - 1
                zera = 0
                licznik = 0
                while j >= 0 and i >= 0:
                    if node.znp_stan[i][j] == node.color:
                        licznik += 1
                    elif node.znp_stan[i][j] != 0:
                        if zera > 0 and licznik > 0 and licznik > ocena:
                            ocena = licznik
                        if licznik >= self.win_state:
                            ocena = licznik
                        licznik = 0
                        zera = 0
                    else:
                        if licznik > ocena:
                            ocena = licznik
                        zera += 1
                        licznik = 0

                    j -= 1
                    i -= 1

                if licznik > ocena:
                    ocena = licznik
        
        node.score = ocena
        node.color = temp_kolor


    def f_ocen_node_bez_ograniczen(self, node, kolor):
        ocena = 0
        temp_kolor = node.color
        node.color = kolor
        for kol in node.znp_stan.T:
            i = len(kol) -1
            licznik = 0
            while i >= 0:
                if kol[i] == node.color:
                    licznik += 1
                elif kol[i] != 0:
                    if licznik >= ocena:
                        ocena = licznik
                    licznik = 0
                else:
                    break
                i -= 1
            if licznik > ocena:
                ocena = licznik

        for wier in node.znp_stan:
            if np.sum(wier) != 0:
                licznik = 0
                zera = 0
                for k in wier:
                    if k == node.color:
                        licznik += 1
                    elif k != 0:
                        if licznik >= ocena:
                            ocena = licznik
                        licznik = 0
                        zera = 0
                    else:
                        if licznik > ocena:
                            ocena = licznik
                        licznik = 0
                        zera += 1
                if licznik > ocena:
                    ocena = licznik

        # przeszukiwanie od dołu na ukos w prawo
        for kol in range(0, len(node.znp_stan[0]) - 1):
            i = len(node.znp_stan) - 1
            j = kol 
            zera = 0
            licznik = 0
            while j < len(node.znp_stan[0]) and i >= 0:
                if node.znp_stan[i][j] == node.color:
                    licznik += 1
                elif node.znp_stan[i][j] != 0:
                    if licznik >= ocena:
                        ocena = licznik
                    licznik = 0
                    zera = 0
                else:
                    if licznik > ocena:
                        ocena = licznik
                    licznik = 0
                    zera += 1
        
                j += 1
                i -= 1

            if licznik > ocena:
                ocena = licznik
        
        # przeszukiwanie od dołu na ukos w lewo
        for kol in range(1, len(node.znp_stan[0])):
            i = len(node.znp_stan) - 1
            j = kol 
            
            zera = 0
            licznik = 0
            while j >= 0 and i >= 0:
                if node.znp_stan[i][j] == node.color:
                    licznik += 1
                elif node.znp_stan[i][j] != 0:
                    if licznik >= ocena:
                        ocena = licznik
                    licznik = 0
                    zera = 0
                else:
                    if licznik > ocena:
                        ocena = licznik
                    licznik = 0
                    zera += 1

                j -= 1
                i -= 1

            if licznik > ocena:
                ocena = licznik

        # przeszukiwanie na ukos w prawo pozostale
        for wier in range(1, len(node.znp_stan) - 1):
            if wier > 0:
                i = wier
                j = 0
                zera = 0
                licznik = 0
                while j < len(node.znp_stan[0]) and i >= 0:
                    if node.znp_stan[i][j] == node.color:
                        licznik += 1
                    elif node.znp_stan[i][j] != 0:
                        if licznik >= ocena:
                            ocena = licznik
                        licznik = 0
                        zera = 0
                    else:
                        if licznik > ocena:
                            ocena = licznik
                        licznik = 0
                        zera += 1

                    j += 1
                    i -= 1

                if licznik > ocena:
                    ocena = licznik
        
        # przeszukiwanie na ukos w lewo pozostale
        for wier in range(1, len(node.znp_stan) - 1):
            if wier > 0:
                i = wier
                j = len(node.znp_stan[0]) - 1
                zera = 0
                licznik = 0
                while j >= 0 and i >= 0:
                    if node.znp_stan[i][j] == node.color:
                        licznik += 1
                    elif node.znp_stan[i][j] != 0:
                        if licznik >= ocena:
                            ocena = licznik
                        licznik = 0
                        zera = 0
                    else:
                        if licznik > ocena:
                            ocena = licznik
                        zera += 1
                        licznik = 0

                    j -= 1
                    i -= 1

                if licznik > ocena:
                    ocena = licznik

        #print(node.znp_stan)
        #print(node.score)
        
        node.score = ocena
        node.color = temp_kolor

        