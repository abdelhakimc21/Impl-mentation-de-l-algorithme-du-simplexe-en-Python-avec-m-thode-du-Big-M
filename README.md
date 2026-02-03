Ce projet implémente l'algorithme du simplexe en Python pour résoudre des problèmes d'optimisation linéaire. Il gère la maximisation et minimisation, les contraintes mixtes (≥, =, ≤) via la méthode du Big M, et affiche les tableaux successifs jusqu'à la solution optimale. Conçu pour un usage académique, le programme guide l'utilisateur pas à pas dans la saisie des coefficients et contraintes, puis retourne la solution optimale avec la valeur de Z.
Exemple d'exécution :

Nombre de variables : 2
Coeff. fonction objectif : 3 5
Nombre de contraintes : 3
Coeff. contrainte 1 : 1 0
Limite contrainte 1 : 4
Type contrainte 1 (>=, =, <=) : <=
Coeff. contrainte 2 : 0 1
Limite contrainte 2 : 6
Type contrainte 2 : <=
Coeff. contrainte 3 : 1 2
Limite contrainte 3 : 18
Type contrainte 3 : <=
Problème de maximisation ? oui

Sortie attendue :
Solution optimale trouvée :
x1 = 4.0
x2 = 6.0
Valeur optimale de Z = 42.0
