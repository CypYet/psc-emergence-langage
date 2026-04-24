import matplotlib.pyplot as plt
from random import *
import random
import numpy as np


Nrobot = 4
Ngeste = 3
n = 1000 #discrétisation du continu
sigma = 0.01
poids = 0.007
n_test = 8000
valeur = np.linspace(0, 1, n)

l = np.array([[[1/n for i in range (n)] for j in range (Ngeste)] for i in range (Nrobot)])

def son(x) :
    return (x + x**2)

def gauss(mu):
    return (1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - ((np.linspace(0, 1, n)) - float(mu))**2 / (2 * sigma**2)))

def update_plus(list, mu):
    list = (list + (poids/n*gauss(mu)))
    list = list / np.sum(list)
    return list

def update_moins (list, mu) :
    list = (list / (1 + 2*poids/n*gauss(mu)))
    list = list / np.sum(list)
    return list


def tirage(list):
    return float(np.random.choice(valeur, 1, p=list))




envergure = son (1) - son(0)
for i in range (n_test) :
    r1 , r2 = random.sample(range(Nrobot), 2) #choix de deux robots distincts
    geste = randint (0, Ngeste - 1) #choix du geste
    g1 , g2 = tirage (l[r1][geste]) , tirage (l[r2][geste]) #choix des paramètres
    if abs(son(g1) - son(g2)) < envergure/10 :
        l[r1][geste] = update_plus(l[r1][geste] , (g1 + g2)/2)  #on renforce le paramètre pour ce geste
        l[r2][geste] = update_plus(l[r2][geste] , (g1 + g2)/2)

        for g in range (Ngeste) : #on affaiblit le paramètre pour les autres gestes de ces même robots
            if g != geste :
                l[r1][g] = update_moins(l[r1][g] , (g1 + g2)/2)
                l[r2][g] = update_moins(l[r2][g] , (g1 + g2)/2)

print(l[0][0])



fig, axes = plt.subplots(Ngeste//3 + min(1,Ngeste%3), 3)
for j in range(Ngeste) :
    for i in range(Nrobot) :
        if Ngeste > 3 :  #disjonction pour raisons techniques (array à une seule dimension si Ngeste <= 3
            axes[j//3,j%3].plot(valeur, l[i][j], label ="robot "+ str(i))
            axes[j//3,j%3].set_title("geste " + str(j))
        else :
            axes[j].plot(valeur, l[i][j], label ="robot "+ str(i))
            axes[j].set_title("geste " + str(j))

plt.tight_layout()
plt.show()




