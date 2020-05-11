"""
Projet d'Étude : Tennis de Table 2020

Ensemble de fonctions pour réaliser la projection d'un objet 3 dans le plan d'une caméra de coordonnées et d'orientation spécifiée.
Ce code doit s'importer dans un autre fichier .py pour aérer le code final.
"""
import numpy as np 
import matplotlib.pyplot as plt 

def pOrtho(M,A,u,v,n=100):
    """
    Projection orthogonale du point M sur le plan (A,u,v)
    n : nombre d'itérations pour faire converger la méthode du gradient

    !!!!!! Les points doivent être des arrays !!!!!!
    """
    H = np.zeros(3)
    H[:] = A
    for i in range(n):
        grad = ((sum(u*(M-H))*u) + (sum(v*(M-H))*v))/10
        H += grad
    return H

def pCentrale(M,S,A,u,v):
    """
    Projection centrale du point M, par rapport au sommet S, sur le plan (A,u,v)
    n : nombre d'itérations pour faire converger la méthode du gradient (dans la fonction pOrtho)

    !!!!!! Les points doivent être des arrays !!!!!!
    """
    P = pOrtho(S,A,u,v,n)
    Q = pOrtho(S,M,u,v,n)
    coeff = np.sqrt(sum((P-S)**2)/sum((Q-S)**2))
    H = S + coeff*(M-S)
    return H

def ProjCam(Object,Cam,A,u,v,axis=None,show=False):
    """
    Projection d'un objet (*Object) (une array de points) dans le plan d'une caméra (*Cam) orienté vers le plan (*A,u,v)
    *axis : axis-object d'une figure matplotlib
    *show : True pour tracer la figure

    !!! La fonction renvoie l'objet projeté dans l'espace 3D !!!
    """
    d,n = np.shape(Object)
    Imag = np.zeros((3,n))
    H = pOrtho(Cam,A,u,v)
    if show:
        axis.plot([H[0]],[H[1]],[H[2]],'r+')
    for i in range(n):
        C = pCentrale(Object[:,i],Cam,A,u,v)
        Imag[:,i] = C
        if show:
            Droite(Cam,Table[:,i],axis)
            axis.plot([C[0]],[C[1]],[C[2]],'ko')
    return Imag

def RefChg(Data,O,u,v,show=False,axis=None,line='k--'):
    """
    Effectue le changement de référentiel 3D -> 2D 
    Les coordonnées des points en entrée (*Data) doivent être déjà dans le plan d'arrivée (O,u,v)
    *show, *axis, *line : optionnels, pour le tracé dans le plan 2D
    """
    d,n = np.shape(Data)
    Ruv = np.zeros((2,n))
    for i in range(n):
        Ruv[0,i] = sum(u*(Data[:,i]-O))
        Ruv[1,i] = sum(v*(Data[:,i]-O))
    if show:
        axis.plot(Ruv[0,:],Ruv[1,:],line)
        axis.plot([0],[0],'r+')
        axis.axis('equal')
    return Ruv