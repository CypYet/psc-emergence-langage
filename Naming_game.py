### Naming game

# On a des robots et des objets. Chaque robot attribue un nom à chaque objet (de manière aléatoire). Puis, les robots communiquent

from random import *
import matplotlib.pyplot as plt
import numpy as np
import math

Nlangage=1000
Nrobot=5
Nmot=9
Niter=1000

robot=[[[] for i in range(Nmot)] for j in range(Nrobot)]

def tirageAleatoire():
    return randint(0,Nlangage-1)

def miseAJour(r,i,mot):
    #le robot r doit augmenter le score du mot mot pour l'objet i
    # il doit aussi diminuer le score du mot mot pour les objets j!=i
    #a la fin, trier la liste
    test=False
    for j in range(len(robot[r][i])):
        if robot[r][i][j][0]==mot:
            robot[r][i][j][1]+=1
            test=True
            k=j
            break
    if not test:
        robot[r][i].append([mot,1])
        k=len(robot[r][i])-1
    while k>0 and robot[r][i][k-1][1]<robot[r][i][k][1]:
        robot[r][i][k-1],robot[r][i][k]=robot[r][i][k],robot[r][i][k-1]
        k-=1
    for j in range(Nmot):
        if j!=i:
            for k in range(len(robot[r][j])):
                if robot[r][j][k][0]==mot:
                    robot[r][j][k][1]-=1
                    if robot[r][j][k][1]==0:
                        robot[r][j].pop(k)
    return

def echange(r1,r2):
    #on pioche un objet (aléatoirement) ;
    #r1 nomme l'objet ;
    #r2 augmente le score du nom donné par r1 pour l'objet i (et diminue les scores des autres)
    i=randint(0,Nmot-1)
    if len(robot[r1][i])==0:
        robot[r1][i].append([tirageAleatoire(),2])
    mot=robot[r1][i][0][0]
    miseAJour(r2,i,mot)
    return True

def distincts(tab):
    visited=[]
    for i in range(len(tab)):
        for j in range(len(tab[i])):
            if not tab[i][j] in visited :
                visited.append(tab[i][j])
    return visited

def meilleurDiv(n):
    res=0
    for i in range(1,int(math.sqrt(n))+1):
        if n%i==0:
            res=i
    return res

def tableau():
    # Palette de couleurs : une couleur par mot
    cmap = plt.get_cmap("tab20")   # 10 couleurs distinctes
    couleurs = {mot: cmap(mot % 10) for mot in range(Nlangage)}

    fig, axes = plt.subplots(3, 3, figsize=(10, 10))

    for i in range(Nmot):

        labels = []
        all_scores = []
        all_words = []

        for r in range(Nrobot):
            mots = [lmot[0] for lmot in robot[r][i]]
            scores = [lmot[1] for lmot in robot[r][i]]

            labels.append(f"Robot {r}")
            all_scores.append(scores)
            all_words.append(mots)

        x = np.arange(Nrobot)
        width = 0.15

        synonymes = distincts(all_words)

        for k, mot in enumerate(synonymes):
            values = [0]*Nrobot
            for r in range(Nrobot):
                for s in range(len(all_words[r])):
                    if all_words[r][s] == mot:
                        values[r] = all_scores[r][s]

            axes[i//3, i%3].bar(
                x + k*width,
                values,
                width,
                label=f"Mot {mot}",
                color=couleurs[mot]   # 🎨 couleur basée sur le mot
            )

        axes[i//3, i%3].set_xticks(x + width*(len(synonymes)-1)/2)
        axes[i//3, i%3].set_xticklabels(labels)
        axes[i//3, i%3].set_ylabel("Score")
        axes[i//3, i%3].set_title(f"Objet {i}")
        axes[i//3, i%3].legend()

    plt.tight_layout()
    plt.show()

def afficher(robot):
    for ligne in robot :
        print(ligne)
    return


def simulation():
    i=0
    while i<Niter:
        r1,r2=randint(0,Nrobot-1),randint(0,Nrobot-1)
        if r1!=r2:
            echange(r1,r2)
            i+=1
    afficher(robot)
    return

simulation()
tableau()

