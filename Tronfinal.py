import random
import time
import copy
import time
import numpy
import numba
from numba import jit

## fenetre d'affichage

import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
plt.ion()
plt.show()
fig,axes = plt.subplots(1,1)
fig.canvas.set_window_title('TRON')


#################################################################################
#
#  Parametres du jeu

LARGEUR = 13
HAUTEUR = 17
L = 20  # largeur d'une case du jeu en pixel

canvas = None   # zone de dessin
Grille = numpy.zeros((LARGEUR,HAUTEUR))   # grille du jeu
PosJ1  = None   # position du joueur 1 (x,y)
#PosJSimu  = None   # position du joueur simule (x,y)
NbPartie = 0   # Nombre de parties effectuées
Scores = [0 , 0]  # score de la partie / total des scores des differentes parties

def InitPartie():  
    global Grille, PosJ1, NbPartie, Scores, PosJSimu
    
    NbPartie += 1
    Scores[0] = 0
    
   
    
    Grille = numpy.zeros((LARGEUR,HAUTEUR))
    
    # #positionne les murs de l'arene
    for x in range(LARGEUR):
       Grille[x][0] = 10
       Grille[x][HAUTEUR-1] = 10
       
    for y in range(HAUTEUR):
       Grille[LARGEUR-1][y] = 10
       Grille[0][y] = 10
       
    for t in range(4) :
        Grille[3][t+3] = 10
        
    for t in range(4) :
        Grille[9][t+3] = 10
        
    for t in range(4) :
        Grille[3][t+10] = 10
        
    for t in range(4) : 
        Grille[9][t+10] = 10
    
    Grille[6][8]=10
    
    # position du joueur 1
    PosJ1 = (LARGEUR//2,1)
    
    # position du joueur simule
    #PosJSimu = (LARGEUR//2,1)


#################################################################################
#
# gestion du joueur humain et de l'IA
# VOTRE CODE ICI 

@jit
def DirectionsPossibles(Grille, x, y) :
  
   Next = []
  
   if (Grille[x][y+1] == 0 ) :
       Next.append((0,1))
   if (Grille[x+1][y] == 0) :
       Next.append((1,0))
   if (Grille[x-1][y] == 0) :
       Next.append((-1,0))
   if (Grille[x][y-1] == 0) :
       Next.append((0,-1))
   
   return Next   

@jit
def SimulationPartie (GrilleTemp,x,y) :
  
   NbCases = 0
   
   while(True) :
    #global PosJSimu
    
    L = DirectionsPossibles(GrilleTemp,x,y)
    
    if ( len(L) == 0 ): return NbCases
    
    rand = random.randrange(len(L))
    Choix = L[rand]
    NbCases+=1
    
    GrilleTemp[x][y] = 1 # laisse la trace de la moto
    
    x = x + Choix[0]
    y = y + Choix[1]
    #PosJSimu = (x, y)  #deplacement
    
    # detection de la collision 
    if ( GrilleTemp[x][y] != 0 ): 
        return NbCases
        
     
@jit
def MonteCarlo(Grille,x,y,NbParties) :  
   Total = 0
   for i in range(NbParties) :
  
           GrilleTemp = numpy.copy(Grille)
           Total += SimulationPartie(GrilleTemp,x,y)
          
   return Total  
   
             
def Play():   
    global Scores
    
    while (True):   

      Tstart = time.time()
      
      global  PosJ1   
      Tot = [0]*4
      BestTot=0
        
      Grille[PosJ1[0]][PosJ1[1]] = 1 # laisse la trace de la moto
      
      DP=DirectionsPossibles(Grille,PosJ1[0],PosJ1[1])
      if(DP) :
        for i in range(len(DP)) :
            Dir=DP[i]
            x = PosJ1[0]+Dir[0]
            y = PosJ1[1]+Dir[1]
            Tot[i]=MonteCarlo(Grille,x,y,10000)
            if (Tot[i] >= BestTot) :
                BestTot=Tot[i]
                GoodDir=Dir
    
        PosJ1 = ( PosJ1[0] + GoodDir[0], PosJ1[1] + GoodDir[1])  #deplacement
      # fin de traitement
      
        Scores[0] +=1
        print(time.time() - Tstart) 
        Affiche()
      
      # detection de la collision  
      
        if ( Grille[PosJ1[0]][PosJ1[1]] != 0 ): return  
       
      else :
          return
    
    
################################################################################
#    
# Dessine la grille de jeu


def Affiche():
    axes.clear()
    
    plt.xlim(0,20)
    plt.ylim(0,20)
    plt.axis('off')
    fig.patch.set_facecolor((0,0,0))
    
    axes.set_aspect(1)
    
    # dessin des murs

    Murs  = []
    Bords = []
    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if ( Grille[x][y] == 10 ) : Bords.append(  plt.Rectangle((x,y), width = 1, height = 1 ) )
           if ( Grille[x][y] == 1  ) : Murs.append(  plt.Rectangle((x,y), width = 1, height = 1 ) )
        
    axes.add_collection (  matplotlib.collections.PatchCollection(Murs,   facecolors = (1.0, 0.47, 0.42)) )
    axes.add_collection (  matplotlib.collections.PatchCollection(Bords,  facecolors = (0.6, 0.6, 0.6)) )
    
    # dessin de la moto
  
    axes.add_patch(plt.Circle((PosJ1[0]+0.5,PosJ1[1]+0.5), radius= 0.5, facecolor = (1.0, 0, 0) ))
    
    # demande reaffichage
    fig.canvas.draw()
    fig.canvas.flush_events()  
 

################################################################################
#    
# Lancement des parties      
          
def GestionnaireDeParties():
    global Scores
   
    for i in range(3):
        time.sleep(1) # pause dune seconde entre chaque partie
        InitPartie()
        Play()
        Scores[1] += Scores[0]   # total des scores des parties
        Affiche()
        ScoMoyen = Scores[1]//(i+1)
        print("Partie " + str(i+1) + " === Score : " + str(Scores[0]) + " === Moy " + str(ScoMoyen) )
        
     
GestionnaireDeParties()

  