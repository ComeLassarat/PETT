# Besoin des fonctions : Table, Projcam, RefChg, 
# Besoin des variables : Data, Cam 
# Si Cam = hauteur cam, il faut le rajouter dans les entrées de la fonction
def anglecam(X0,Y0,Xtab,Ytab):
    theta = -90 # Valeur de départ
    Ytab = (Ytab-Y0)*0,761/(Xtab-Ytab)
    u = np.array([np.cos(theta*np.pi/180),0,np.sin(theta*np.pi/180)])
    v = np.array([0,1,0])
    A = Table[:,2]
    I = ProjCam(Data,Cam,A,u,v)
    R = RefChg(I,I[:,3],v,-u) # R[1][5] la valeur de Ytab pour thata = -90°
    while abs(R[1][5]-Ytab)>0.01: # Boucle pour obtenir theta à 0.1° près.
        if R[1][5]-Ytab[3]<0:
            theta-=0.1
        else:
            theta+=0.1
        u = np.array([np.cos(theta*np.pi/180),0,np.sin(theta*np.pi/180)])
        v = np.array([0,1,0])
        A = Table[:,2]
        I = ProjCam(Data,Cam,A,u,v)
        R = RefChg(I,I[:,3],v,-u)
   return theta 
