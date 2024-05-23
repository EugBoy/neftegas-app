import tkinter as tk
from tkinter import *
import numpy as np

root = tk.Tk()
root.title("Расчёт коэффициента сверхсжимаемости газа")
root.geometry("800x500")
root.resizable(False, False)
photo = tk.PhotoImage(file="favicon.png")
root.iconphoto(False, photo)
# Делаем вес каждой колонки = 1
for i in range(12):
    root.columnconfigure(index=i, weight=1)

tk.Label(root, text="Исходные данные").grid(row=0, column=0, columnspan=6, stick='ew')
tk.Label(root, text="Результат расчёта").grid(row=0, column=6, columnspan=6, stick='ew')

tk.Label(root, text="Компонент").grid(row=1, column=1, columnspan=2, pady=(15, 0))
tk.Label(root, text="Мольная доля, %").grid(row=1, column=3, columnspan=2, pady=(15, 0))

# Create a vertical Frame
vertical = Frame(root, bg="black", height=500, width=2)
vertical.place(x=400, y=0)

# Create a horizontal Frame
horizontal = Frame(root, bg="black", height=1, width=800)
horizontal.place(x=0, y=20)

# Create a horizontal Frame
horizontal1 = Frame(root, bg="black", height=1, width=400)
horizontal1.place(x=400, y=240)

horizontal1 = Frame(root, bg="black", height=1, width=400)
horizontal1.place(x=0, y=310)

tk.Label(root, text="C1").grid(row=2, column=1, columnspan=2, pady=(0, 5))
C1 = tk.Entry(root)
C1.insert(0, 98.22)
C1.grid(row=2, column=3, columnspan=2)

tk.Label(root, text="C2").grid(row=3, column=1, columnspan=2, pady=(0, 5))
C2 = tk.Entry(root)
C2.insert(0, 0.95)
C2.grid(row=3, column=3, columnspan=2)

tk.Label(root, text="C3").grid(row=4, column=1, columnspan=2, pady=(0, 5))
C3 = tk.Entry(root)
C3.insert(0, 0.55)
C3.grid(row=4, column=3, columnspan=2)

tk.Label(root, text="NC4").grid(row=5, column=1, columnspan=2, pady=(0, 5))
NC4 = tk.Entry(root)
NC4.insert(0, 0)
NC4.grid(row=5, column=3, columnspan=2)

tk.Label(root, text="NC5").grid(row=6, column=1, columnspan=2, pady=(0, 5))
NC5 = tk.Entry(root)
NC5.insert(0, 0)
NC5.grid(row=6, column=3, columnspan=2)

tk.Label(root, text="C6").grid(row=7, column=1, columnspan=2, pady=(0, 5))
C6 = tk.Entry(root)
C6.insert(0, 0)
C6.grid(row=7, column=3, columnspan=2)

tk.Label(root, text="N2").grid(row=8, column=1, columnspan=2, pady=(0, 5))
N2 = tk.Entry(root)
N2.insert(0, 0)
N2.grid(row=8, column=3, columnspan=2)

tk.Label(root, text="CO2").grid(row=9, column=1, columnspan=2, pady=(0, 5))
CO2 = tk.Entry(root)
CO2.insert(0, 0.2)
CO2.grid(row=9, column=3, columnspan=2)

tk.Label(root, text="H2S").grid(row=10, column=1, columnspan=2, pady=(0, 5))
H2S = tk.Entry(root)
H2S.insert(0, 0.08)
H2S.grid(row=10, column=3, columnspan=2)

tk.Label(root, text="Пластовое давление, МПа").grid(row=11, column=1, columnspan=2, pady=(50, 0))
PP = tk.Entry(root)
PP.insert(0, 6.57045)
PP.grid(row=11, column=3, columnspan=2, pady=(50, 0))

tk.Label(root, text="Пластовая температура, K").grid(row=12, column=1, columnspan=2, pady=(10, 0))
PT = tk.Entry(root)
PT.insert(0, 307)
PT.grid(row=12, column=3, columnspan=2, pady=(10, 0))

tk.Button(root, text='Рассчитать', command=lambda: calcZ()).grid(row=13, column=2, columnspan=2, sticky='ew', pady=(40, 0))

tk.Label(root, text="По СРК:").grid(row=3, column=7, columnspan=2)
z1 = tk.StringVar()
z1.set('')

SRK = tk.Entry(root, textvariable=z1, state='readonly')
SRK.grid(row=3, column=9, columnspan=2)

tk.Label(root, text="По П-Р:").grid(row=5, column=7, columnspan=2)
z2 = tk.StringVar()
z2.set('')

PPR = tk.Entry(root, textvariable=z2, state='readonly')
PPR.grid(row=5, column=9, columnspan=2)

tk.Label(root, text="По Гуревичу-Платонову:").grid(row=10, column=7, columnspan=2)
z3 = tk.StringVar()
z3.set('')
PGP = tk.Entry(root, textvariable=z3, state='readonly')
PGP.grid(row=10, column=9, columnspan=2)

tk.Label(root, text="Критическое давление, МПа:").grid(row=11, column=7, columnspan=2, pady=(50, 0))
Pc = tk.StringVar()
Pc.set('')

PC = tk.Entry(root, textvariable=Pc, state='readonly')
PC.grid(row=11, column=9, columnspan=2, pady=(50, 0))

tk.Label(root, text="Критическая температура, K:").grid(row=12, column=7, columnspan=2, pady=(10, 0))
Tc = tk.StringVar()
Tc.set('')

TC = tk.Entry(root, textvariable=Tc, state='readonly')
TC.grid(row=12, column=9, columnspan=2, pady=(10, 0))



# Разделить массив на подмамассивы(сделать матрицу)
def split_array(array, num):
    new_array = [array[i:i + num] for i in range(0, len(array), num)]
    return new_array


def calcZ():
    # Исходные данные
    xj = [
        float(C1.get())/100, float(C2.get())/100, float(C3.get())/100,
        float(NC4.get())/100, float(NC5.get())/100, float(C6.get())/100,
        float(N2.get())/100, float(CO2.get())/100, float(H2S.get())/100
    ]
    xk = xj

    R = 8.314

    Tпл = float(PT.get())

    Pпл = float(PP.get())*1000000

    Tcj = [190.45, 305.32, 369.83, 425.12, 469.7, 512.8, 126.2, 304.19, 373.53]

    Vcj = [0.0000986, 0.0001455, 0.0002, 0.000255, 0.000313, 0.000335]

    Vck = [0.0000986, 0.0001455, 0.0002, 0.000255, 0.000313, 0.000335]

    Pcj = [45.99 * 100000, 48.72 * 100000, 42.48 * 100000, 37.96 * 100000, 33.7 * 100000, 33.3 * 100000, 34.6 * 100000,
           73.82 * 100000, 89.63 * 100000]

    w = [0.012, 0.1, 0.152, 0.2, 0.252, 0.25, 0.0377, 0.228, 0.0942]

    # ------------------------------------------------------------------------------------

    # Расчёт aj для П-Р
    aj1 = []
    for j in range(9):
        aj1.append(0.45724 * (R ** 2) * (Tcj[j] ** 2) / Pcj[j])

    # ------------------------------------------------------------------------------------
    # Расчёт aj для СРК
    aj2 = []
    for j in range(9):
        aj2.append(0.42748 * (R ** 2) * (Tcj[j] ** 2) / Pcj[j])

    # ------------------------------------------------------------------------------------

    # Расчёт bj ДЛЯ П-Р
    bj1 = []
    for j in range(9):
        bj1.append(0.0778 * (R) * (Tcj[j]) / Pcj[j])

    # ------------------------------------------------------------------------------------
    # Расчёт bj ДЛЯ СРК
    bj2 = []
    for j in range(9):
        bj2.append(0.08664 * (R) * (Tcj[j]) / Pcj[j])

    # ------------------------------------------------------------------------------------

    # Расчёт kj ДЛЯ П-Р
    kj1 = []
    for j in range(9):
        kj1.append(0.37464 + 1.54226 * w[j] - 0.26992 * (w[j] ** 2))

    # ------------------------------------------------------------------------------------
    # Расчёт kj ДЛЯ СРК
    kj2 = []
    for j in range(9):
        kj2.append(0.48 + 1.574 * w[j] - 0.176 * (w[j] ** 2))

    # ------------------------------------------------------------------------------------

    # Расчёт alpha_j ДЛЯ П-Р
    alpha_j1 = []
    for j in range(9):
        alpha_j1.append(aj1[j] * ((1 + kj1[j] * (1 - ((Tпл / Tcj[j]) ** 0.5))) ** 2))

    alpha_k1 = alpha_j1

    # ------------------------------------------------------------------------------------

    # Расчёт alpha_j ДЛЯ СРК
    alpha_j2 = []
    for j in range(9):
        alpha_j2.append(aj2[j] * ((1 + kj2[j] * (1 - ((Tпл / Tcj[j]) ** 0.5))) ** 2))

    alpha_k2 = alpha_j2

    # ------------------------------------------------------------------------------------

    # Расчёт delta для углеводородных компонентов
    delta_test = []

    delta = []

    for j in range(6):
        for k in range(6):
            delta_test.append(1 - (((2 * ((Vcj[j] ** (1 / 6)) * (Vck[k] ** (1 / 6)))) / (
                    (Vcj[j] ** (1 / 3)) + (Vck[k] ** (1 / 3)))) ** (1.2)))

    delta_test = np.array(split_array(delta_test, 6))

    delta.append(np.block([delta_test[0], np.array([0.025, 0.105, 0.07])]))
    delta.append(np.block([delta_test[1], np.array([0.01, 0.13, 0.085])]))
    delta.append(np.block([delta_test[2], np.array([0.09, 0.125, 0.08])]))
    delta.append(np.block([delta_test[3], np.array([0.095, 0.115, 0.075])]))
    delta.append(np.block([delta_test[4], np.array([0.1, 0.115, 0.07])]))
    delta.append(np.block([delta_test[5], np.array([0.11, 0.115, 0.07])]))
    delta.append(np.array([0.025, 0.01, 0.09, 0.095, 0.1, 0.11, 0, 0, 0.13]))
    delta.append(np.array([0.105, 0.13, 0.125, 0.115, 0.115, 0.115, 0, 0, 0.135]))
    delta.append(np.array([0.07, 0.085, 0.08, 0.075, 0.07, 0.07, 0.13, 0.135, 0]))
    # ------------------------------------------------------------------------------------

    # Расчёт alpha_jk для П-Р
    alpha_jk1 = []

    for j in range(9):
        for k in range(9):
            alpha_jk1.append(((alpha_j1[j] * alpha_k1[k]) ** 0.5) * (1 - delta[j][k]))

    alpha_jk1 = split_array(alpha_jk1, 9)

    # ------------------------------------------------------------------------------------

    # Расчёт alpha_jk для СРК
    alpha_jk2 = []

    for j in range(9):
        for k in range(9):
            alpha_jk2.append(((alpha_j2[j] * alpha_k2[k]) ** 0.5) * (1 - delta[j][k]))

    alpha_jk2 = split_array(alpha_jk2, 9)

    # ------------------------------------------------------------------------------------

    # Расчёт alpha_m и betta_m для П-Р
    xjxk = (np.outer(xj, xk))

    alpha_m1 = np.sum(np.array(xjxk) * np.array(alpha_jk1))

    betta_m1 = np.sum(np.dot(xj, bj1))

    # ------------------------------------------------------------------------------------
    # Расчёт alpha_m и betta_m для СРК
    alpha_m2 = np.sum(np.array(xjxk) * np.array(alpha_jk2))

    betta_m2 = np.sum(np.array(xj) * np.array(bj2))

    # ------------------------------------------------------------------------------------

    # Расчёт A и B для П-Р
    A1 = (alpha_m1 * Pпл) / ((R ** 2) * (Tпл ** 2))

    B1 = (betta_m1 * Pпл) / ((R) * (Tпл))

    # ------------------------------------------------------------------------------------

    # Расчёт A и B для СРК
    A2 = (alpha_m2 * Pпл) / ((R ** 2) * (Tпл ** 2))

    B2 = (betta_m2 * Pпл) / ((R) * (Tпл))

    # ------------------------------------------------------------------------------------

    # Расчёт z для П-Р
    coeff1 = [1, -(1 - B1), (A1 - 2 * B1 - 3 * (B1 ** 2)), -(A1 * B1 - ((B1 ** 2) - (B1 ** 3)))]

    global z1

    z1.set(max([np.real(x) for x in np.roots(coeff1)]))

    PPR.insert(0, z1)

    print("z ПО П-Р = ", z1)
    # ------------------------------------------------------------------------------------

    # Расчёт z для СРК
    coeff2 = [1, -(1), (A2 - 1 * B2 - 1 * (B2 ** 2)), -(A2 * B2)]

    global z2

    z2.set(max([np.real(x) for x in np.roots(coeff2)]))

    print("z ПО СРК = ", z2)

    SRK.insert(0,z2)

    # Расчёт z для Гуревичу-Платонову
    m = [16.043, 30.07, 44.097, 58.123, 72.15, 84, 28.013, 44.01, 34.082]

    Mj = []

    for j in range(9):
        Mj.append(m[j] * xj[j])

    M = np.sum(Mj)

    print("M =", M)

    #Pс = (0.006894 * (709.604 - (M / 28.96) * 58.718))
    global Pc
    Pc.set(np.sum(np.array(xj) * np.array(Pcj))/1000000)
    PC.insert(0, Pc)

    global Tc
    Tc.set(np.sum(np.array(xj) * np.array(Tcj)))
    TC.insert(0, Tc)

    #Tс = ((170.491 + (M / 28.96) * 307.44) / 1.8)
    Pc = np.sum(np.array(xj) * np.array(Pcj))
    Tc = np.sum(np.array(xj) * np.array(Tcj))
    global z3

    z3.set((0.4 * np.emath.log10((Tпл / Tc)) + 0.73) ** (Pпл / Pc) + 0.1 * (Pпл / Pc))

    print("z3 = ", z3)

    PGP.insert(0, z3)

root.mainloop()
