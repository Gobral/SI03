from c_bot import C_Bot
import numpy as np

znp_plansza = np.zeros((6,7), np.int8)
znp_plansza[5][4] = 1
znp_plansza[5][5] = 2
znp_plansza[5][6] = 1
znp_plansza[4][5] = 1
znp_plansza[4][4] = 2
znp_plansza[3][4] = 1
znp_plansza[5][3] = 2
znp_plansza[4][3] = 2

print(znp_plansza)
zb_bot1 = C_Bot(znp_plansza, 1, 4)
zb_bot2 = C_Bot(znp_plansza, 2, 4)
znp_plansza = zb_bot1.f_wykonaj_ruch(znp_plansza)
print(znp_plansza)
znp_plansza = zb_bot2.f_wykonaj_ruch(znp_plansza)
print(znp_plansza)
znp_plansza = zb_bot1.f_wykonaj_ruch(znp_plansza)
print(znp_plansza)
znp_plansza = zb_bot2.f_wykonaj_ruch(znp_plansza)
print(znp_plansza)
znp_plansza = zb_bot1.f_wykonaj_ruch(znp_plansza)
print(znp_plansza)
znp_plansza = zb_bot2.f_wykonaj_ruch(znp_plansza)
print(znp_plansza)
znp_plansza = zb_bot1.f_wykonaj_ruch(znp_plansza)
print(znp_plansza)
znp_plansza = zb_bot2.f_wykonaj_ruch(znp_plansza)
print(znp_plansza)