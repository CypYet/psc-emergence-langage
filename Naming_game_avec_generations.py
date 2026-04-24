### Naming game

# On a des robots et des objets. Chaque robot attribue un nom à chaque objet (de manière aléatoire). Puis, les robots communiquent. On ajoute un système de générations

from random import *
import matplotlib.pyplot as plt
import numpy as np
import math

Nlangage=1000
Nrobot=8
Nmot=9
Niter=1000
Nages=10
Ngeneration=2


robot=[[[] for i in range(Nmot)] for j in range(Nrobot)]

def tirageAleatoire():
    return randint(0,Nlangage-1)

def nouvelleGen():
    robot[:Nrobot//Ngeneration]=robot[Nrobot//Ngeneration:].copy()
    robot[Nrobot//Ngeneration:]=[[[] for i in range(Nmot)] for j in range(Nrobot//Ngeneration)]
    for i in range(Nrobot//Ngeneration):
        for j in range(Nmot):
            if random()<0.05:
                x=tirageAleatoire()
                robot[Nrobot//Ngeneration+i][j]=[[x,2]]
    return

def miseAJour(r,i,mot,score):
    #le robot r doit augmenter le score du mot mot pour l'objet i
    # il doit aussi diminuer le score du mot mot pour les objets j!=i
    #a la fin, trier la liste
    #version avec deux générations qui communiquent : si le mot reçu par le robot (qui est de la dernière génération) provient d'un robot de la même génération que lui, le score augmente plus.
    test=False
    for j in range(len(robot[r][i])):
        if robot[r][i][j][0]==mot:
            robot[r][i][j][1]+=score
            test=True
            k=j
            break
    if not test:
        robot[r][i].append([mot,1])
        k=len(robot[r][i])-1
    while k>0 and robot[r][i][k-1][1]<robot[r][i][k][1]:
        robot[r][i][k-1],robot[r][i][k]=robot[r][i][k],robot[r][i][k-1]
        k-=1
    for t in range(Nmot):
        if len(robot[r][t])!=0 and t!=i:
            s=0
            while s<len(robot[r][t]):
                if len(robot[r][t][s])!=0 and robot[r][t][s][0]==mot:
                    robot[r][t][s][1]-=1
                    if robot[r][t][s][1]==0:
                        robot[r][t].pop(s)
                s+=1
    return

def echange(r1,r2,score):
    #on pioche un objet (aléatoirement) ;
    #r1 nomme l'objet ;
    #r2 augmente le score du nom donné par r1 pour l'objet i (et diminue les scores des autres)
    i=randint(0,Nmot-1)
    if len(robot[r1][i])==0:
        robot[r1][i].append([tirageAleatoire(),2])
    mot=robot[r1][i][0][0]
    miseAJour(r2,i,mot,score)
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
    # robot[r][i] = liste de [mot, score] pour le robot r et l'objet i
    Nfig=meilleurDiv(Nmot)
    fig, axes = plt.subplots(3,3)  # à remplacer
    for i in range(Nmot):

        # Pour chaque robot, on récupère les mots et scores
        labels = []
        all_scores = []
        all_words = []

        for r in range(Nrobot):
            mots = [lmot[0] for lmot in robot[r][i]]
            scores = [lmot[1] for lmot in robot[r][i]]

            labels.append(f"Robot {r}")
            all_scores.append(scores)
            all_words.append(mots)

        # On crée un barplot groupé
        x = np.arange(Nrobot)
        width = 0.15  # largeur des barres

        # Trouver le nombre max de mots pour aligner les groupes
        synonymes = distincts(all_words)

        for k in range(len(synonymes)):
            values = [0]*len(robot)
            for r in range(Nrobot):
                for s in range(len(all_words[r])):
                    if all_words[r][s]==synonymes[k]:
                        values[r]=all_scores[r][s]

            axes[i//3,i%3].bar(x + k*width, values, width, label=f"Mot {synonymes[k]}")

        plt.xticks(x + width*(len(synonymes)-1)/2, labels)
        plt.ylabel("Score")
        axes[i//3,i%3].legend()
        plt.tight_layout()
    plt.show()


def tableau2():
    cmap = plt.get_cmap("tab20")   # 10 couleurs distinctes
    couleurs = {mot: cmap(mot%20) for mot in range(Nlangage)}

    labels = []
    all_scores = []
    all_words = []

    for r in range(Nrobot):
        mots = [lmot[0] for lmot in robot[r][0]]
        scores = [lmot[1] for lmot in robot[r][0]]

        labels.append(f"Robot {r}")
        all_scores.append(scores)
        all_words.append(mots)

    # On crée un barplot groupé
    x = np.arange(Nrobot)
    width = 0.15  # largeur des barres

    # Trouver le nombre max de mots pour aligner les groupes
    synonymes = distincts(all_words)

    for k in range(len(synonymes)):
        values = [0]*len(robot)
        for r in range(Nrobot):
            for s in range(len(all_words[r])):
                if all_words[r][s]==synonymes[k]:
                    values[r]=all_scores[r][s]

        plt.bar(x + k*width, values, width, label=f"Mot {synonymes[k]}",color=couleurs[synonymes[k]])

    plt.xticks(x + width*(len(synonymes)-1)/2, labels)
    plt.ylabel("Score")
    plt.legend()
    plt.tight_layout()
    plt.show()

def afficher(robot):
    for ligne in robot :
        print(ligne)
    return


def simulation():
    afficher(robot)
    i=0
    while i<Nages:
        nouvelleGen()
        j=0
        while j<Niter:
            r2,r1=randint(Nrobot//Ngeneration,Nrobot-1),randint(0,Nrobot-1)
            if r1!=r2:
                if r1<Nrobot//Ngeneration:
                    score=1
                else:
                    score=4
                echange(r1,r2,score)
                j+=1
        plt.figure(i)
        tableau2()
        i+=1
    afficher(robot)
    return

simulation()

