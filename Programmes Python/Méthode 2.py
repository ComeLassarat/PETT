import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import random as rd


# Pas et nombre de points simulés
h = 10**(-3)
n = 600
n2=n+1
#Table
L = 2.74
l = 1.522
H = 0.1525
Table = np.array([[0,0,L,L,0,0  ,L  ,L ,L/2,L/2,L/2,L/2,L/2],
				  [0,l,l,0,0,l/2,l/2,0 ,0  ,0  ,l  ,l  ,0],
				  [0,0,0,0,0,0  ,0  ,0 ,0  ,H  ,H  ,0  ,0]])
d1, n1 = np.shape(Table)
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
def simulation(E):
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

#Trajectoire pointée qu'on nous donne
Xp=[0.54,0.58,0.63,0.67,0.71,0.74,0.78,0.83,0.87,0.91,0.94,0.96,0.99,1]
Yp=[0.3,0.38,0.47,0.50,0.55,0.57,0.58,0.58,0.56,0.55,0.61,0.67,0.73,0.77]
Pp=[Xp,Yp]
# plt.plot(Xp,Yp)
# plt.show()

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


def reelcam(Pos):               #Fonction permettant de passer les coordonnées réelles de la trajectoire simulée (3D) dans le plan 2D caméra. Paramètres comme caméra et theta et A a modifier dans fonction.
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

def Table2D(Table):
    Traj = np.zeros((3,len(Table[0])))
    Traj[0,:] = Table[0]
    Traj[1,:] = Table[1]
    Traj[2,:] = Table[2]
    I = ProjCam(Traj,Cam,A,u,v)
    R = RefChg(I,I[:,3],v,-u)
    Ps=[R[0,:],R[1,:]]
    return(Ps)

def coos(E):
    Pos=simulation(E)   #Simule trajectoire; extrait liste coordonnées 3D Pos=[X1,Y1,Z1]
    Ps=echantillone(Pos)
    Pss=reelcam(Ps)
    return(Pss)

def echantillone(Pos):      # Réduit liste coordonnées 2D simulées au bon nombre de points par rapport à Pp
    #print(n2)
    k=len(Pos[0])//(len(Xp)-1)
    Xss,Yss,Zss=[],[],[]
    #print(len(Pos[0])
    for i in range(len(Xp)-1):
        Xss.append(Pos[0][k*i])
        Yss.append(Pos[1][k*i])
        Zss.append(Pos[2][k*i])
    Xss.append(Pos[0][-1])
    Yss.append(Pos[1][-1])
    Zss.append(Pos[2][-1])
    return([Xss,Yss,Zss])

def Einitial():
    x=-0.6+3.45*rd.random()
    y=-0.25+2*rd.random()
    z=-0.3+0.6*rd.random()
    vx=15*rd.random()
    vy=-5+10*rd.random()
    vz=-8+16*rd.random()
    return([x,y,z,vx,vy,vz,0,0,0])

def ecartinitial(Pp,Pss):
    return(((Pp[0][0]-Pss[0][0])**2+(Pp[1][0]-Pss[1][0])**2)**0.5)

def fginitial(E,Pp):              #Prend en entrée E=[Xo,V,Omega] et renvoye l'écart norme entre la trajectoire pointée et celle simulée dans plan2D
    Pos=simulation(E)   #Simule trajectoire; extrait liste coordonnées 3D Pos=[X1,Y1,Z1]
    Ps=echantillone(Pos)
    Pss=reelcam(Ps)
    e=ecartinitial(Pp,Pss)
    return(e)


def grad(E,s): #a modifier en fonction des axes utilisés (pour l'instant z haut x longeur table, y largeur table)
    gra=np.zeros(9)
    if s==0:
        e=fginitial(E,Pp)
    if s==1:
        e=fg(E,Pp)

    if s==0:
        dx=0.02     #Pour le petit déplacement en position dx, on impose une même valeur à peu près égal à 1/100 ordre de grandeur en position(=2m)
        FF=[E[0]+dx,E[1],E[2],E[3],E[4],E[5],E[6],E[7],E[8]]
        ff=fginitial(FF,Pp)
        gra[0]=(ff-e)/dx

        GG=[E[0],E[1]+dx,E[2],E[3],E[4],E[5],E[6],E[7],E[8]]
        gg=fginitial(GG,Pp)
        gra[1]=(gg-e)/dx

        HH=[E[0],E[1],E[2]+dx,E[3],E[4],E[5],E[6],E[7],E[8]]
        hh=fginitial(HH,Pp)
        gra[2]=(hh-e)/dx
#Pour le petit déplacement en vitesse, on prend des valeurs différentes car les vitesse selon les axes sont très différentes: la vitesse selon x est très impportant donc on prend dvx=0,2
    if s==1:
        II=[E[0],E[1],E[2],E[3]+0.02,E[4],E[5],E[6],E[7],E[8]]
        ii=fg(II,Pp)
        gra[3]=(ii-e)/0.02

        JJ=[E[0],E[1],E[2],E[3],E[4]+0.002,E[5],E[6],E[7],E[8]]
        jj=fg(JJ,Pp)
        gra[4]=(jj-e)/0.002

        KK=[E[0],E[1],E[2],E[3],E[4],E[5]+0.005,E[6],E[7],E[8]]
        kk=fg(KK,Pp)
        gra[5]=(kk-e)/0.005
    #print('dw')
    #dw=1.5#Pour le petit déplacement en effet dw, on impose une même valeur à peu près égal à 1/100 ordre de grandeur en effet(=)rad/s
    # LL=[E[0],E[1],E[2],E[3],E[4],E[5],E[6]+dw,E[7],E[8]]
    # ll=fg(LL,Pp)
    # gra[6]=(ll-e)/dw

   #   MM=[E[0],E[1],E[2],E[3],E[4],E[5],E[6],E[7]+dw,E[8]]
    # mm=fg(MM,Pp)
    # gra[7]=(mm-e)/dw

   #NN=[E[0],E[1],E[2],E[3],E[4],E[5],E[6],E[7],E[8]+dw]
    # nn=fg(NN,Pp)
    # gra[8]=(nn-e)/dw
    return(gra)


def ecart(Pp,Pss):              #Fonction calculant écart entre trajectoires 2D pointées et celle simulée
    e=0
    for i in range (len(Pp[0])):
        e=e+((Pp[0][i]-Pss[0][i])**2+(Pp[1][i]-Pss[1][i])**2)**0.5

    return(e)

def fg(E,Pp):              #Prend en entrée E=[Xo,V,Omega] et renvoye l'écart norme entre la trajectoire pointée et celle simulée dans plan2D
    Pos=simulation(E)   #Simule trajectoire; extrait liste coordonnées 3D Pos=[X1,Y1,Z1]
    Ps=echantillone(Pos)
    Pss=reelcam(Ps)
    #print(Pp)
    #print(Pss)
    e=ecart(Pp,Pss)
    return(e)

def choixdelta(FGG):
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
    A=Einitial() #Vecteur d'Etat: Pos,Vit,Effet E=[Xo,Yo,Zo,Vxo,Vyo,Vzo,wxo,wyo,wzo] pris au hasard
    E=A
    gamma=0.1
    erreurinitial=[]

    n=0
    FG=fginitial(E,Pp)
    s=0

    while FG>0.01:
        print(n)
        print(FG)
        Q=grad(E,s)
        E=E-gamma*Q
        erreurinitial.append(FG)
        FG=fginitial(E,Pp)
        if FG>0.02 and FG<0.04:
            gamma=0.08
        if FG<0.02:
            gamma=0.008
        if FG<0.009:
            gamma=0.005
        n=n+1
    erreurinitial.append(FG)
    print('FIN INITIAL')
    s=1
    Epos=E
    m=0
    y=90
    FGG=fg(Epos,Pp)
    erreur=[FGG,FGG]
    delta=choixdelta(FGG)
    print(y)
    print(FGG)
    while (FGG>0.005 and m<y) or abs(FGG-erreur[-1])>0.06:
        print(m)
        print(FGG)
        Q=grad(E,s)
        E=E-delta*Q
        erreur.append(FGG)
        FGG=fg(E,Pp)
        m=m+1
        delta=choixdelta(FGG)

    erreur.append(FGG)
    print('FINNNNN')
    return(A,E,Epos,n,erreurinitial,erreur)



# def pgr():
#     erf=[]
#     E=[]
#     KK=[]
#     for i in range (20):
#         GG,FFF,SSS,n,erri,K=moindrecarré(Pp)
#         erf.append(K[-1])
#         print(n)
#         print(K[-1])
#         E.append(FFF)
#         KK.append(K)
#     return(E,erf,KK)

#E,erf,KK=pgr()

# for i in KK[0:6]:
#     L=[k for k in range(len(i))]
#     plt.plot(L,i)
#     plt.show()
#
#
# z=min(erf)
# for i in range(len(erf)):
#     if erf[i]==z:
#         k=i
#         S=E[i]
#
#
# D=S.tolist()

Table2D=Table2D(Table)

#GG,FFF,SSS,n,erri,K=moindrecarré(Pp)

FF=FFF.tolist()
SS=SSS.tolist()

print(n)
print('Einitial')
print(GG)
print('Efinal')
print(FF)
print('Eposition')
print(SS)
print('erreur')
print(K)



F=coos(FF)
XF=F[0]
YF=F[1]
G=coos(GG)
XG=G[0]
YG=G[1]

S=coos(SS)
XS=S[0]
YS=S[1]

plt.figure(1)
plt.plot(Table2D[0],Table2D[1],'bo')
plt.plot(Table2D[0],Table2D[1],'k-')
plt.plot(XF,YF,'g.',label='finale')
plt.legend()
plt.plot(XG,YG,'r.',label='initiale')
plt.legend()
plt.plot(XS,YS,'c.',label='pos')
plt.legend()

plt.plot(Xp,Yp,label='original pointée')
plt.legend()
plt.show()

plt.figure(2)
L=[i for i in range(len(K))]
plt.plot(L,K)
plt.show()