from c_bot import C_Bot
import numpy as np
import tkinter as tk




def f_wykonaj_ruch_bota():
    global indeks
    global graj
    global znp_plansza
    if graj and (znp_plansza.shape[0] * znp_plansza.shape[1]) - np.count_nonzero(znp_plansza) > 0:
        zwrot = gracze[indeks].f_wykonaj_ruch(znp_plansza)
        znp_plansza = zwrot[0]
        graj = zwrot[1]
        print(znp_plansza)
        for i in range(0, len(znp_plansza)):
            for j in range(0, len(znp_plansza[0])):
                if znp_plansza[i][j] == 1:
                    labele[i][j].configure(bg = "red")
                elif znp_plansza[i][j] == 2:
                    labele[i][j].configure(bg = "yellow")
        if indeks == 0:
            indeks = 1
        else:
            indeks = 0

window = tk.Tk()
window.title("Czwórki")
window.geometry("345x400")

znp_plansza = np.zeros((6,7), np.int8)
zb_bot1 = C_Bot(znp_plansza, 1, 4)
zb_bot2 = C_Bot(znp_plansza, 2, 4)
gracze = [zb_bot1, zb_bot2]

graj = True
indeks = 0

labele = []
for i in range(2, 8):
    row = []
    for j in range(0, 7):
        label = tk.Button(text='', height = 2, width = 4)
        label.grid(row = i, column = j, padx = 5, pady = 5)
        row.append(label)
    labele.append(row)

bot_ruch_button = tk.Button(text='Ruch bota', command=f_wykonaj_ruch_bota, height = 2, width = 8)
bot_ruch_button.grid(row = 10, column = 3, columnspan = 2, padx = 5, pady = 5)

window.mainloop()

