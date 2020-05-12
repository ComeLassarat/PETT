## État actuel de la tâche

Un jeu de données à été créé et annoté pour entrainer un algorithme de machine learning. On utilise le module [Tensorflow](https://www.tensorflow.org) de Google pour réaliser l'entrainement et ensuite utiliser le modèle ainsi entrainé.

### Premiers résultats

Actuellement, le modèle à été entrainé sur 1800 images, et pour plus de 20 000 étapes (étapes avec traitement de 30 images par étape, bridé par les capacités de l'ordinateur utilisé (RAM : 8Go) et plus d'une semaine d'entrainement (pas de GPU pouvant supporter le module Tensorflow). Du fait de ces nombreux soucis rencontrés, l'algorithme n'arrive pas à une perte (i.e. Total Loss) inférieure à 3 (min : 2.96) alors qu'une perte au-dessous de 2 (au moins !) est recommandée.
De plus lors de l'utilisation de l'algorithme, la balle n'est non seulement jamais reconnue, mais il n'y a jamais de tentative d'identifier celle-ci, alors que les joueurs sont plutôt bien identifiés (illustration à venir). Cela pourrait être du à une erreur dans le format de données en entrée de l'algorithme, bien que plusieurs pistes restent à explorer pour comprendre et corriger si possible l'algorithme sous sa forme actuelle.
