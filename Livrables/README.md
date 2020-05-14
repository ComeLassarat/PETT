# Projet d'étude : Tennis de Table

Ce dossier regroupe tous les documents relatifs aux livrables du projet

### 1. Gestion de projet 

Cette partie concerne la gestion globale du projet avec les RVP1&2 et le rapport final.

### 2. Acquisition

Les acquisitions faites dans un premier temps à l'aide de l'outil de Motion Capture, qui a été abandonné car trop complexe et divergent de notre objectif final : fournir une application capable d'analyser une partie, et d'en déduire les tendances d'un joueurs.

### 3. Mouvement de la balle 

Cette partie concerne l'analyse du mouvement de la balle, dans des situations classiques du tennis de table, afin d'en tirer un modèle pour simulation.

Tâches | Description 
:-----: | :-----------------------------------------------------------------
3.1 | État de l'art du tennis de table, caractérisation des coups possibles et de la physique de ces coups.
3.2 | Définition d'une trajectoire théorique de balle, élaboration d'un modèle.
3.3 | **Livrable 2 :** Synthèse.

### 4. Programmes et simulations

On élabore ensuite des programmes pour faire des calculs basiques sur des trajectoires 3D, calculs qui seront en définitive utiles pour l'identification d'un "style de jeu".

Tâches | Description 
:-----: | :-----------------------------------------------------------------
4.1 | Programme permettant le calcul de vitesse de la balle, angle de rebond, etc.. à partir de la trajectoire 3D.
4.2 | Simulation de la physique de balle, uniquement avec en entrée la vitesse et position initiale du lancer.

### 5. Analyse de la trajectoire 

On réalise dans cette partie la partie pratique du projet : l'identification de la trajectoire de la balle (3D) à partir d'une vidéo (2D), impliquant un tracking de la balle sur la vidéo. On réalise ensuite une analyse de la trajectoire identifiée selon le modèle fournit par la FFTT. 

Tâches | Description 
:-----: | :-----------------------------------------------------------------
5.1 | Projection d'une trajectoire en 3D sur un plan, dans le but d'obtenir une vue caméra de la trajectoire 3D.
5.2 | Détermination de la position de la caméra à partir de la forme de la table vue dans le plan de la caméra.
5.3 | Tracking automatique de la balle image par image. Obtention d'une trajectoire en 2D.
5.4 | Identification d'une trajectoire 3D à partir de la trajectoire 2D vue dans le plan de la caméra.
5.5 | Traitement et analyse des données récoltées. 
5.6 | Catégorisation des coups automatique.
5.7 | **Livrable 3 :** Analyse d'une trajectoire à partir d'une vidéo et élaboration de statistiques
