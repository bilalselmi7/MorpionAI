# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 15:49:18 2020

@author: SELMI Bilal and KANOUTE Cheick
"""
from math import inf
from random import choice,randint
import time
#import numpy as np

humain = 1 # utilisateur
ia = -1 # ordinateur
table = [[0,0,0], # table de jeu contenant que des cases vides de base
         [0,0,0],
         [0,0,0]]

#def grille():          Créer une grille de la taille saisie par l'utilisateur mais erreur car np
#    try:
#        a=int(input("Choisissez la taille de la grille de départ : "))
#        print(a)
#    except (ValueError) or (a==0) :
#        print("Erreur")
#       
#    A = np.random.randint(1, size=(a,a))
#    print(A)
#    return A
###############################################################################################################
def cases_vides(plateau):
    """
    Toutes les cases vides du jeu sont entrées dans une liste (cases)
    plateau : état actuel du jeu
    return : une liste contenant toutes les cellules vides du jeu
    
    """
    cases=[] #  liste qui va contenir les cases vides
    for x,ligne in enumerate(plateau): # on parcourt le tableau en ligne
        for y,case in enumerate(ligne):
            if case == 0 : # si la case est vide
                cases.append([x,y]) # on entre ses coordonnées dans la liste
    return cases
###############################################################################################################
def result(x,y,joueur):
    """
    Permet de placer le pion du joueur actuel sur la table de jeu
    En vérifiant bien qu'il s'agisse uniquement d'une case vide
    x : coordonnée en ligne
    y : coordonnée en colonne
    joueur : joueur actuel
    
    """
    if [x,y] in cases_vides(table):  # Si la case est vide 
        table[x][y] = joueur         # On peut placer le pion du joueur
        return True                  # On le place
    else : 
        return False                 # On ne le place pas
###############################################################################################################
def victoire(plateau,joueur):
    """
    Permet de tester si un joueur gagne la partie
    plateau : état actuel du jeu
    joueur : joueur actuel
    
    """
    #gagner = [[plateau[i][j]for i in range 2]for j in range 2]
    gagner = [
             [plateau[0][0],plateau[1][0],plateau[2][0]], # Colonne 1
             [plateau[0][1],plateau[1][1],plateau[2][1]], # Colonne 2
             [plateau[0][2],plateau[1][2],plateau[2][2]], # Colonne 3
             [plateau[0][0],plateau[0][1],plateau[0][2]], # Ligne 1
             [plateau[1][0],plateau[1][1],plateau[1][2]], # Ligne 2
             [plateau[2][0],plateau[2][1],plateau[2][2]], # Ligne 3
             [plateau[0][0],plateau[1][1],plateau[2][2]], # Diagonale 1
             [plateau[2][0],plateau[1][1],plateau[0][2]], # Diagonale 2              
             ]
    if [joueur,joueur,joueur] in gagner : # Si le même joueur a placé un pion dans une des positions gagnantes
        return True                       # précisées au-dessus, on renvoie True (il a gagné)
    else : 
        return False                      # Sinon il n'a pas gagné
###############################################################################################################
def fin(plateau):
    """
    Permet de déterminer qui a gagné la partie
    plateau : état actuel du jeu
    return : True si quelqu'un a gagné
    """
    return victoire(plateau,humain) or victoire(plateau,ia) # Le jeu est fini si l'un des deux joueurs gagnent
###############################################################################################################
def utility(plateau):
    """
    Permet de calculer le score
    plateau : état actuel du jeu
    return : -1 si l'humain gagne, 1 si l'ordinateur gagne, 0 si égalité
    
    """
    if victoire(plateau,humain): 
        score = -1
    if victoire(plateau,ia):
        score = 1
    else :
        score = 0
    return score
###############################################################################################################
def minimax(plateau,profondeur,joueur):
    """
    Se base sur la méthode Minimax et le principe d'élagage afin de sélectionner
    le meilleur coup pour l'IA
    plateau : état actuel du jeu
    profondeur : profondeur de l'arbre d'élagage qui sera donc comprise entre 0 et 9 (9:grille vide,0:grille pleine)
    joueur : joueur actuel
    return : une liste [meilleure ligne, meilleure colonne, meilleur score]
    """
    if joueur == ia:       
        choix = [-1,-1,-inf]
        
    else :        
        choix = [-1,-1,+inf]
        
    if profondeur == 0 or fin(plateau): # Si le jeu est fini (i.e quelqu'un a gagné ou le plateau est rempli)     
        score = utility(plateau) 
        return [-1,-1,score]
    
    for case in cases_vides(plateau): # On parcourt les cases vides 
        x,y = case[0],case[1]
        plateau[x][y] = joueur
        score = minimax(plateau,profondeur -1, joueur) # Recursivite avec profondeur -1 car on place un pion
        plateau[x][y]=0
        score[0],score[1]=x,y  
        
        if joueur == ia: 
            a=randint(0,2)
            if score[a] > choix[a]:             
                choix = score
        else:            
            if score[a] < choix[a]:               
                choix = score
    
    return choix
###############################################################################################################
def Minimax(plateau,joueur):
    #dico={i:MinVal(Result(grille,i)) for i in Actions(grille)}
    #return dico
    vmin=+inf
#    for case in cases_vides(plateau):
#        x,y=case[0],case[1]
    for i in cases_vides(plateau):
        if(vmin>MinVal(result(plateau,i,joueur))):
            vmin = MinVal(result(plateau,i,joueur))
            best = i        
    return best
###############################################################################################################
def MaxVal(plateau):
    if fin(plateau): return utility(plateau)
    v=-inf
    for i in cases_vides(plateau):
        v=max(v,MinVal(result(plateau,i)))
    return v
###############################################################################################################
def MinVal(plateau):
    if fin(plateau): return utility(plateau)
    v=+inf
    for i in cases_vides(plateau):
        v=min(v,MaxVal(result(plateau,i)))
    return v
###############################################################################################################
def Affichage(plateau,ordi,hum):
    """
    Affiche le jeu
    plateau : état actuel du jeu
    ordi : pion de l'ordinateur
    hum : pion de l'humain
    """
    car = {-1:hum , 1: ordi, 0: ' '}
    print("\n----------------")
    for ligne in plateau:
        for case in ligne:
            pion = car[case]
            print(f'| {pion} |',end='')
        print("\n----------------")
#    for ligne in plateau:
#        for case in ligne:
#            if ordi:
#                pion = 'X'
#            else: 
#                pion = 'O'
#            print(pion,end='')
#    for i in range(len(plateau)):
#        for j in range(len(plateau)):
#            print(plateau[i][j],end='')
###############################################################################################################
def tour_humain(ordi,hum):
    """
    Permet à l'utilisateur de placer un pion
    ordi : pion de l'ordinateur
    hum : pion de l'humain
    
    """
    profondeur = len(cases_vides(table)) # La profondeur correspond au nombre de cases vides restantes
    if profondeur == 0 or fin(table): # Si le jeu est fini (profondeur = 0 donc plus de cases ou il y a un gagnant)
        return
    place = 0
    choix = {                       # On crée un dictionnaire des indexs possibles
              1 : [0,0], #Case 1,2,.....
              2 : [0,1],
              3 : [0,2],
              4 : [1,0],
              5 : [1,1],
              6 : [1,2],
              7 : [2,0],
              8 : [2,1],
              9 : [2,2],
            }
    #clean()
    print("Tour joueur")
    Affichage(table,ordi,hum)
    while place < 1 or place > 9: # Tant que le pion n'a pas une position valable
        try:
            place = int(input('Choisissez une case entre 1 et 9 :\n'))
            coordonnee = choix[place]
            possible = result(coordonnee[0],coordonnee[1],humain)
            
            if not possible:
                print('Entrez une case disponible\n')
                place = 0
        except(KeyError,ValueError):
            print("Entrez une case disponible\n")
############################################################################################################   
def tour_ia(ordi,hum):
    """
    Appelle la fonction minimax si la profondeur est < 9 sinon choisit une case aléatoire
    ordi : pion de l'ordinateur
    hum : pion de l'humain
    
    """
    profondeur = len(cases_vides(table))
    if profondeur == 0 or fin(table):
        return
    #clean()
    print("Tour de l'Ordinateur")
    Affichage(table,ordi,hum)
    if profondeur == 9:
        x = choice([0,1,2]) # 2 façons de faire aléatoirement
        y = choice([0,1,2])
        x=randint(0,2)
        y=randint(0,2)
    else :
        choix = minimax(table,profondeur,ia)
        #choix=Minimax(table,ia)
        x , y = choix[0], choix[1]
    result(x,y,ia)
    time.sleep(1)
###########################################################################################################    
def main():
    """
    Main du programme qui appelle toutes les fonctions
    """
    hum = ''
    ordi = ''
    premier = ''
    
    while hum != 'O' and hum != 'X':
        try:
            hum = input("Choisissez 'X' ou 'O'\n").upper() # On choisit si le pion est X ou O
        except(ValueError):
            print("Choisissez 'X' ou 'O'\n")
    
    if hum == 'X':
        ordi = 'O' # L'ordinateur prend l'autre pion
    else:
        ordi = 'X'
        
    while premier != '1' and premier != '2':
        try:
            premier = input("Qui commence ?\nJoueur : 1\nOrdinateur : 2\n").upper() # On choisit qui commence
        except(ValueError):
            print("Qui commence ?\nJoueur : 1\nOrdinateur : 2\n")
    
    while len(cases_vides(table)) > 0 and not fin(table): # Tant qu'il reste des cases vides ou jeu non fini
        if premier == '2': # Si l'ordinateur commence
            tour_ia(ordi,hum) # Il joue
            premier = ''
        tour_humain(ordi,hum) # Humain puis ia
        tour_ia(ordi,hum)
    if victoire(table,humain): # Victoire HUMAIN
        Affichage(table,ordi,hum)
        print("Victoire")
    elif victoire(table,ia):   # Victoire ORDINATEUR
        Affichage(table,ordi,hum)
        print("Défaite")
    else:                      # Aucune Victoire (match nul)
        Affichage(table,ordi,hum)
        print("Egalite")
#####################################################################################################          
if __name__ == '__main__':
    main()

    
    

