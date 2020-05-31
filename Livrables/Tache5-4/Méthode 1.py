import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

# Pas et nombre de points simulés. Choisis de telle sorte que n*h=t avec t le temps du coup pointé.
h = 0.0028
n = 200

#Table
L = 2.74
l = 1.522
H = 0.1525
Table = np.array([[0,0,L,L,0,0  ,L  ,L ,L/2,L/2,L/2,L/2,L/2],
				  [0,l,l,0,0,l/2,l/2,0 ,0  ,0  ,l  ,l  ,0],
				  [0,0,0,0,0,0  ,0  ,0 ,0  ,H  ,H  ,0  ,0]])
d1, n1 = np.shape(Table)
#axes utilisés (pour l'instant z haut x longeur table, y largeur table)

#Caméra    paramètres pour le passage du plan 3D à celui de la caméra
Theta = -90 #(°)
u = np.array([np.cos(Theta*np.pi/180),0,np.sin(Theta*np.pi/180)])
v = np.array([0,1,0])
A = Table[:,2]
Cam = np.array([6.50,l/2,1.50])


#=============== Paramètres de la simulation =============#
alpha = 1.2*(10**(-3))  #Coeff de frottement visqueux
m = 2.7*(10**(-3))      #Masse Balle
g = 9.81                #Champ gravitationnel
magnus = 1.8*(10**(-4)) #Coeff Magnus
µ = 0.2526              #Frottement au rebond
r = 2*10**(-2)          #Rayon balle

def vect(u,v):  #Simplifie les expressions (produit vectoriel)
    w = np.zeros(3)
    w[0] = u[1]*v[2]-u[2]*v[1]
    w[1] = u[2]*v[0]-u[0]*v[2]
    w[2] = u[0]*v[1]-u[1]*v[0]
    return w

def f(U,w):     #Fonction pour la méthode d'Euler
    du = U[0,:]
    d2u = -alpha*(np.sqrt(sum(du*du)))*du/m - g*np.array([0,0,1]) + magnus*vect(w,du)
    return np.array([d2u,du])

def norm(a):    #Simplifie également (norme 2)
    n = np.sqrt(sum(a**2))
    return n

def e(vz):      #Coeff de restitution en fonction de Vz
    Vz = abs(vz)
    if Vz<1.9:
        return 0.93
    else:
        return 1 - 0.037*Vz

#=============== Gestion du rebond ====================#
def rebond(U,r,w):  #Fonction qui permet de gérer le rebond
    Vc = U[0,:] + vect(np.array([0,0,r]),w)
    E = e(U[0,2])
    beta = 2.5*µ*(1+E)*abs(U[0,2])/norm(Vc)
    if beta>=1: ###Cas de Roulement
        tau = 0.4       #tau correspond au symbole alpha dans la théorie
        c = (1-tau)/r   # (ou le symbole proportionnel)
        d = tau
    else:       ###Cas de Glissement
        tau = beta/2.5
        c = 3*tau/(2*r)
        d = 1 - 3*tau/2
    THETA = np.zeros((6,6))
    A = np.diagflat([1-tau,1-tau,-E])
    B = np.diagflat([tau*r,0],1) + np.diagflat([-tau*r,0],-1)
    C = np.diagflat([-c,0],1) + np.diagflat([c,0],-1)
    D = np.diagflat([d,d,1])
    THETA[0:3,0:3] = A
    THETA[0:3,3:6] = B #A et B sont les mêmes quelque soit beta
    THETA[3:6,0:3] = C #C et D changent d'ou les variables c et d
    THETA[3:6,3:6] = D
    VW = np.zeros(6)
    VW[0:3] = U[0,:]
    VW[3:6] = w
    VW2 = np.dot(THETA,VW) #Multiplication matricielle
    return VW2

#================== Simulation =====================#
def simulation(E):          #imule la trajectoire 3D théorique correspondant au vecteur initial E
    #print('Simulation :',n*h,'s')
    U0=np.array([[E[3],E[4],E[5]],[E[0],E[1],E[2]]])  #U0=[Vit,Pos]
    wo=[E[6],E[7],E[8]]                     #vecteur rotation
    X = [U0[1,0]]      #Initialise liste coordonées trajectoire
    Y = [U0[1,1]]
    Z = [U0[1,2]]
    for p in range(n): #Application de la méthode d'Euler
        U0 = U0 + h*f(U0,wo)
        z0 = U0[1,2]
        X.append(U0[1,0])
        Y.append(U0[1,1])
        Z.append(U0[1,2]) #Cas d'un rebond :
        if z0<10**(-3) and sum(U0[0]*np.array([0,0,1]))<=0:
                VW = rebond(U0,r,wo)
                U0[0,:] = VW[0:3]
                wo = VW[3:6]
    Pos=[X,Y,Z]
    return(Pos)




#Trajectoire pointée que l'on cherche à identifier
#Traj1:
#Xp=[0.54,0.58,0.63,0.67,0.71,0.74,0.78,0.83,0.87,0.91,0.94,0.96,0.99,1]
#Yp=[0.3,0.38,0.47,0.50,0.55,0.57,0.58,0.58,0.56,0.55,0.61,0.67,0.73,0.77]

#Traj2
#Xp=[0.982,0.916,0.842,0.763,0.699,0.623,0.551,0.481,0.395,0.32,0.25,0.18,0.106,0.0454,-0.02216]
#Yp=[0.776,0.754,0.725,0.673,0.628,0.557,0.494,0.408,0.312,0.215,0.129,0.141,0.146,0.135,0.122]

#SErvice
#Xp=[0.896,0.865,0.848,0.8349,0.8172,0.7927,0.7682,0.7324,0.7144,0.6852,0.647,0.6153,0.586,0.5458]
#Yp=[0.8724,0.7726,0.6438,0.6283,0.6418,0.6375,0.6221,0.5867,0.5535,0.4959,0.425,0.3341,0.2543,0.2323]


#Coup 3
Xp=[0.6622,0.7644,0.8489,0.9372,1.017,1.132,1.217,1.311,1.411,1.511,1.586]
Yp=[1.16,1.09,0.9911,0.906,0.781,0.5465,0.3568,0.2021,0.1522,0.06734,-0.00325]


Pp=[Xp,Yp]

#Fonctions utiles pour le passage du plan 3D au plan 2D
def pOrtho(M,A,u,v,n=100):
    H = np.zeros(3)
    H[:] = A
    for i in range(n):
        grad = ((sum(u*(M-H))*u) + (sum(v*(M-H))*v))/10
        H += grad
    return H

H = pOrtho(Cam,A,u,v)


def pCentrale(M,S,A,u,v):
    P = pOrtho(S,A,u,v)
    Q = pOrtho(S,M,u,v)
    coeff = np.sqrt(sum((P-S)**2)/sum((Q-S)**2))
    H = S + coeff*(M-S)
    return H

def ProjCam(Object,Cam,A,u,v,axis=None,show=False):
    d,n = np.shape(Object)
    Imag = np.zeros((3,n))
    for i in range(n):
        C = pCentrale(Object[:,i],Cam,A,u,v)
        Imag[:,i] = C
    return Imag

def RefChg(Data,O,u,v,show=False):
    d,n = np.shape(Data)
    Ruv = np.zeros((2,n))
    for i in range(n):
        Ruv[0,i] = sum(u*(Data[:,i]-O))
        Ruv[1,i] = sum(v*(Data[:,i]-O))
    return Ruv


def reelcam(Pos):        #Fonction permettant de passer les coordonnées réelles de la trajectoire simulée (3D) dans le plan 2D caméra.
    Traj = np.zeros((3,len(Pos[0])))
    Traj[0,:] = Pos[0]
    Traj[1,:] = Pos[1]
    Traj[2,:] = Pos[2]
    H = pOrtho(Cam,A,u,v)

    Ref=np.array([2.74,0,0])
    I = ProjCam(Traj,Cam,A,u,v)
    R = RefChg(I,Ref,v,-u)
    Ps=[R[0,:],R[1,:]]
    return(Ps)


def Table2D(Table):  #Fonction permettant de passer les coordonnées réelles de la table dans le plan 2D caméra.
    Traj = np.zeros((3,len(Table[0])))
    Traj[0,:] = Table[0]
    Traj[1,:] = Table[1]
    Traj[2,:] = Table[2]
    I = ProjCam(Traj,Cam,A,u,v)
    R = RefChg(I,I[:,3],v,-u)
    Ps=[R[0,:],R[1,:]]
    return(Ps)



def ecart(Pp,Pss):              #Fonction calculant écart entre trajectoires 2D pointées et celle simulée
    e=0
    for i in range (len(Pp[0])):
        e=e+((Pp[0][i]-Pss[0][i])**2+(Pp[1][i]-Pss[1][i])**2)**0.5
    return(e)


def fg(E,Pp):       #Prend en entrée E=[Xo,V,Omega] et renvoye l'écart norme entre la trajectoire pointée et celle simulée dans plan2D
    Pos=simulation(E)   #Simule trajectoire; extrait liste coordonnées 3D Pos=[X1,Y1,Z1]
    Ps=echantillone(Pos)#Réduit liste 3D au bon nombre de points
    Pss=reelcam(Ps)     #Passe coordonnées 3D en 2D
    e=ecart(Pp,Pss)     #calcul l'écart entre les trajectoires
    return(e)


def grad(E): #renvoie en sortie le gradient pour le vecteur E
    gra=np.zeros(9)
    e=fg(E,Pp)
    dx=0.02         #Pour le petit déplacement en position dx, on impose une même valeur à peu près égal à 1/100 ordre de grandeur en position(=2m)

    FF=[E[0]+dx,E[1],E[2],E[3],E[4],E[5],E[6],E[7],E[8]]
    ff=fg(FF,Pp)
    gra[0]=(ff-e)/dx

    GG=[E[0],E[1]+dx,E[2],E[3],E[4],E[5],E[6],E[7],E[8]]
    gg=fg(GG,Pp)
    gra[1]=(gg-e)/dx

    HH=[E[0],E[1],E[2]+dx,E[3],E[4],E[5],E[6],E[7],E[8]]
    hh=fg(HH,Pp)
    gra[2]=(hh-e)/dx
#Pour le petit déplacement en vitesse, on prend des valeurs différentes car les vitesse selon les axes sont très différentes: la vitesse selon x est très impportant donc on prend dvx=0,2
    II=[E[0],E[1],E[2],E[3]+0.2,E[4],E[5],E[6],E[7],E[8]]
    ii=fg(II,Pp)
    gra[3]=(ii-e)/0.2

    JJ=[E[0],E[1],E[2],E[3],E[4]+0.02,E[5],E[6],E[7],E[8]]
    jj=fg(JJ,Pp)
    gra[4]=(jj-e)/0.02

    KK=[E[0],E[1],E[2],E[3],E[4],E[5]+0.05,E[6],E[7],E[8]]
    kk=fg(KK,Pp)
    gra[5]=(kk-e)/0.05

    #Les résultats de la méthode 1 n'étant pas du tout concluant on ne prend pas le temps de simuler l'impact de l'effet
    return(gra)


def coos(E):   #fonction qui reprend la fonction fg mais que l'on utilise jute pour plot ce qui nous intéresse
    Pos=simulation(E)   #Simule trajectoire; extrait liste coordonnées 3D Pos=[X1,Y1,Z1]
    Ps=echantillone(Pos)
    Pss=reelcam(Ps)
    return(Pss)

def choixdelta(FGG):       #Fonction pour accélérer le processus. Plus l'erreur est grande plus on va prendre un pas grand.
    if FGG<0.6:
        d=0.1
    if FGG>0.6 and FGG<0.8:
        d=0.2
    if FGG>0.8 and FGG<1:
        d=0.3
    if FGG>1 and FGG<1.2:
        d=0.4
    if FGG>1.2 and FGG<1.7:
        d=0.5
    if FGG>1.5 and FGG<3:
        d=0.6
    if FGG>3 and FGG<6:
        d=1.1
    if FGG>6:
        d=1.5
    return(d)

def moindrecarré(Pp):
    E=[1,0,1,0,1,1,0,0,0]  #Vecteur d'Etat: Pos,Vit,Effet E=[Xo,Yo,Zo,Vxo,Vyo,Vzo,wxo,wyo,wzo] pris au hasard

    erreur=[]
    n=0
    FG=fg(E,Pp)
    while FG>0.01 and n<200:
        print(n)
        print(FG)
        gamma=choixdelta(FG)   #choix du pas en fonction de l'erreur
        Q=grad(E)
        #print(Q)
        E=E-gamma*Q
        #print(E)
        erreur.append(FG)
        FG=fg(E,Pp)
        n=n+1
    return(E,n,erreur)

Table2D=Table2D(Table)  #calcule coordonnées table en 2D caméra

GG,n,K=moindrecarré(Pp) #calcule vecteur initial trouvé, nombre d itération et vecteur erreur

print(n)
print('Efinal')
print(GG)
print('erreur')
print(K)

F=coos(GG)
XF=F[0]
YF=F[1]

plt.figure(1)
plt.plot(Table2D[0],Table2D[1],'bo')
plt.plot(Table2D[0],Table2D[1],'k-')
plt.plot(XF,YF,'r.',label='Trajectoire théorique')
plt.plot(XF,YF,'r')

plt.title('Trajectoire pointée et simulée par la théorie dans le plan de la caméra')
plt.legend()

plt.plot(Xp,Yp,label='Trajectoire pointée')
plt.plot(Xp,Yp,'b.')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

plt.figure(2)
L=[i for i in range(len(K[2:]))]
plt.plot(L,K[2:])
plt.xlabel('Nombre d itération')
plt.ylabel('Erreur')
plt.title('Evolution de l erreur entre la trajectoire simulée et celle pointée')
plt.show()

#Remarque: A chaque fois, l'erreur àà la deuxième itération est très grande. Je ne comprends pas pourquoi