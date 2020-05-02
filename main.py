from c_bot import C_Bot
import numpy as np

znp_plansza = np.zeros((6,7), np.int8)
zb_bot = C_Bot(znp_plansza, 1)
print(znp_plansza)