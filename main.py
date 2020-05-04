from c_bot import C_Bot
import numpy as np

znp_plansza = np.zeros((6,7), np.int8)


print(znp_plansza)
zb_bot1 = C_Bot(znp_plansza, 1, 4)
zb_bot2 = C_Bot(znp_plansza, 2, 4)
gracze = [zb_bot1, zb_bot2]
indeks = 0

graj = True
while graj and (znp_plansza.shape[0] * znp_plansza.shape[1]) - np.count_nonzero(znp_plansza) > 0:
    zwrot = gracze[indeks].f_wykonaj_ruch(znp_plansza)
    znp_plansza = zwrot[0]
    graj = zwrot[1]
    print(znp_plansza)
    if indeks == 0:
        indeks = 1
    else:
        indeks = 0
