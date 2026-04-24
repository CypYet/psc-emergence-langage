import matplotlib.pyplot as plt
import random
import numpy as np


n = 1000
robot1, robot2 = np.array([1/n for i in range (n)]), np.array([1/n for i in range (n)])
valeur = np.linspace(0, 1, n)
sigma = 0.005
poids = 0.1
n_test = 10000
curiosite = 0.2 # distance minimale acceptée entre le nouveau son produit par un robot donné, et le son que ce même robot a produit précédemment.



def tirage(proba):
    return float(np.random.choice(valeur, p=proba))


def update(proba, mu):
    gauss = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - ((np.linspace(0, 1, n)) - float(mu))**2 / (2 * sigma**2))
    proba = (proba + (poids/n*gauss))
    proba = proba / np.sum(proba)
    return proba

t1 = (tirage(robot1))
t2 = (tirage(robot2))

for i in range (n_test) :
    t = tirage(robot1)   #choix du son par le robot1
    while abs(t-t1) < curiosite:
        t = tirage(robot1)
    t1 = t
    robot2 = update(robot2, t1)

    t = tirage(robot2)  #choix du son par le robot 2
    while abs(t-t2) < curiosite:
        t = tirage(robot2)
    t2 = t
    robot1 = update(robot1, t2)



plt.plot(valeur, robot1, label ="robot 1")
plt.plot(valeur, robot2, label ="robot 2")
plt.title(f"Distributions de probabilité de son des robots. \n \u03C3 = {sigma}, poids = {poids}, n_étapes = {n_test}, curiosite = {curiosite}. " , fontsize = 15) # j'ai modifié la signification du poids pour pouvoir expliquer ce qu'il veut dire
plt.legend()
plt.show()
