from c_bot import C_Bot
from c_node import C_Node
import numpy as np
import tkinter as tk
from tkinter import messagebox
from functools import partial
import time

def f_wykonaj_ruch_bota():
    global indeks
    global graj
    global znp_plansza
    delta = 0
    if graj and (znp_plansza.shape[0] * znp_plansza.shape[1]) - np.count_nonzero(znp_plansza) > 0:
        zwrot = gracze[indeks].f_wykonaj_ruch(znp_plansza)
        znp_plansza = zwrot[0]
        graj = zwrot[1]
        delta = zwrot[2]
        #print(znp_plansza)
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
        
        if not graj:
            messagebox.showinfo("Powiadomienie", "Rozgrywka zakończona, wygrywa gracz " + ("czerwony" if indeks == 1 else "żółty"))
    else:
        print("Koniec gry")
    return delta

def f_ruch_czlowieka(x):
    global indeks
    global graj
    ilosc = len(znp_plansza) - np.count_nonzero(znp_plansza.T[x])
    if graj and (znp_plansza.shape[0] * znp_plansza.shape[1]) - np.count_nonzero(znp_plansza) > 0:
        if ilosc > 0:
            if indeks == 0:
                znp_plansza[ilosc - 1][x] = 1
                indeks = 1
            else:
                znp_plansza[ilosc - 1][x] = 2
                indeks = 0
            
            node = C_Node(znp_plansza)

            gracze[0].f_ocen_node(node, 1)
            if node.score >= 4:
                graj = False
            gracze[0].f_ocen_node(node, 2)

            if node.score >= 4:
                graj = False
            
            if not graj:
                messagebox.showinfo("Powiadomienie", "Rozgrywka zakończona, wygrywa gracz " + ("czerwony" if indeks == 1 else "żółty"))

            
            for i in range(0, len(znp_plansza)):
                for j in range(0, len(znp_plansza[0])):
                    if znp_plansza[i][j] == 1:
                        labele[i][j].configure(bg = "red")
                    elif znp_plansza[i][j] == 2:
                        labele[i][j].configure(bg = "yellow")
    else:
        print("Koniec gry")

def f_automatyzuj_boty():
        global graj
    #for i in range(0, 100):
        ruvhy = 0
        czas = 0
        while graj and (znp_plansza.shape[0] * znp_plansza.shape[1]) - np.count_nonzero(znp_plansza) > 0:
            czas += f_wykonaj_ruch_bota()
            ruvhy += 1
            window.update()
        print("statystki:", ruvhy, czas/ruvhy)
        #f_resetuj_plansze()

def f_resetuj_plansze():
    global indeks
    global graj
    global znp_plansza
    znp_plansza = np.zeros((6,7), np.int8)
    graj = True
    indeks = 0
    for i in range(0, len(znp_plansza)):
        for j in range(0, len(znp_plansza[0])):
            labele[i][j].configure(bg = "SystemButtonFace")
        

window = tk.Tk()
window.title("Czwórki")
window.geometry("345x400")

znp_plansza = np.zeros((6,7), np.int8)
zb_bot1 = C_Bot(znp_plansza, 1, 4)
zb_bot2 = C_Bot(znp_plansza, 2, 4)
gracze = [zb_bot1, zb_bot2]

graj = True
indeks = 0

k0 = tk.Button(text = "V", command=partial(f_ruch_czlowieka, 0), height = 1, width = 4)
k0.grid(row = 1, column = 0, padx = 5, pady = 5)
k1 = tk.Button(text = "V", command=partial(f_ruch_czlowieka, 1),  height = 1, width = 4)
k1.grid(row = 1, column = 1, padx = 5, pady = 5)
k2 = tk.Button(text = "V", command=partial(f_ruch_czlowieka, 2), height = 1, width = 4)
k2.grid(row = 1, column = 2, padx = 5, pady = 5)
k3 = tk.Button(text = "V", command=partial(f_ruch_czlowieka, 3), height = 1, width = 4)
k3.grid(row = 1, column = 3, padx = 5, pady = 5)
k4 = tk.Button(text = "V", command=partial(f_ruch_czlowieka, 4), height = 1, width = 4)
k4.grid(row = 1, column = 4, padx = 5, pady = 5)
k5 = tk.Button(text = "V", command=partial(f_ruch_czlowieka, 5), height = 1, width = 4)
k5.grid(row = 1, column = 5, padx = 5, pady = 5)
k6 = tk.Button(text = "V", command=partial(f_ruch_czlowieka, 6), height = 1, width = 4)
k6.grid(row = 1, column = 6, padx = 5, pady = 5)

labele = []
for i in range(2, 8):
    row = []
    for j in range(0, 7):
        label = tk.Button(text='', height = 2, width = 4)
        label.grid(row = i, column = j, padx = 5, pady = 5)
        row.append(label)
    labele.append(row)

bot_ruch_button = tk.Button(text='Ruch bota', command=f_wykonaj_ruch_bota, height = 2, width = 8)
bot_ruch_button.grid(row = 10, column = 0, columnspan = 2, padx = 5, pady = 5)

bot_reset_button = tk.Button(text='Resetuj', command=f_resetuj_plansze, height = 2, width = 8)
bot_reset_button.grid(row = 10, column = 2, columnspan = 2, padx = 5, pady = 5)

bot_ai_button = tk.Button(text='AI vs AI', command=f_automatyzuj_boty, height = 2, width = 8)
bot_ai_button.grid(row = 10, column = 4, columnspan = 2, padx = 5, pady = 5)

window.mainloop()

