def obtenir_entrees_utilisateur():
    """Récupère les entrées utilisateur."""
    n = int(input("Nombre de variables : "))
    c = list(map(float, input(f"Coeff. fonction objectif (séparés par espace) : ").split()))
    m = int(input("Nombre de contraintes : "))

    A = []
    b = []
    types_contraintes = []

    for i in range(m):
        ligne = list(map(float, input(f"Coeff. contrainte {i + 1} (séparés par espace) : ").split()))
        A.append(ligne)
        limite = float(input(f"Limite contrainte {i + 1} : "))
        b.append(limite)
        type_contrainte = input(f"Type contrainte {i + 1} (>=, =, <=) : ")
        types_contraintes.append(type_contrainte)

    maximisation = input("Problème de maximisation (oui/non) ? ").lower() == 'oui'
    return c, A, b, types_contraintes, maximisation

def tableau_initial_simplexe(c, A, b, types_contraintes, maximisation, M=1e10):
    """Crée le tableau initial du simplexe avec 'M' symbolique."""
    m = len(A)
    n = len(c)
    tableau = []

    # Initialisation des variables
    z_row = [0] * (n + m + m + 1)  # Coefficients de la fonction objectif
    for i in range(m):
        if types_contraintes[i] in ('>=', '='):
            z_row[n + m + i] = -M  # Ajout de Big M pour les variables artificielles

    # Ajout des contraintes au tableau
    for i in range(m):
        contrainte = A[i][:]
        if b[i] < 0:
            contrainte = [-val for val in contrainte]
            b[i] = -b[i]

        ajout = [0] * m + [0] * m
        if types_contraintes[i] == '>=':
            ajout[i] = -1  # Variable d'excédent
            ajout[m + i] = 1  # Variable artificielle
        elif types_contraintes[i] == '=':
            ajout[m + i] = 1  # Variable artificielle
        elif types_contraintes[i] == '<=':
            ajout[i] = 1  # Variable d'écart

        tableau.append(contrainte + ajout + [b[i]])

    # Ajout de la ligne de la fonction objectif à la fin
    tableau.append(z_row)

    return tableau

def evaluer_expression(expression):
    """Évalue une expression contenant 'M' si possible."""
    if isinstance(expression, (int, float)):
        return expression
    try:
        return eval(expression.replace('M', '1e10'))  # Remplace M par une grande valeur pour l'évaluation
    except (NameError, SyntaxError, TypeError, ZeroDivisionError):
        return expression  # Retourne l'expression telle quelle si elle ne peut pas être évaluée

def colonne_pivot(tableau):
    """Trouve la colonne pivot."""
    min_val = float('inf')
    min_index = -1
    for i, val in enumerate(tableau[-1][:-1]):  # Dernière ligne pour Z
        val_eval = evaluer_expression(val)
        if isinstance(val_eval, (int, float)) and val_eval < min_val:
            min_val = val_eval
            min_index = i
    return min_index

def ligne_pivot(tableau, col):
    """Trouve la ligne pivot."""
    ratios = []
    for i in range(len(tableau) - 1):  # Exclure la dernière ligne
        diviseur = evaluer_expression(tableau[i][col])
        if not isinstance(diviseur, (int, float)) or diviseur <= 0:
            continue
        ratio = evaluer_expression(tableau[i][-1]) / diviseur
        ratios.append((ratio, i))

    if not ratios:
        return None
    return min(ratios)[1]

def pivot(tableau, ligne, col):
    """Effectue le pivot."""
    pivot_val = tableau[ligne][col]
    tableau[ligne] = [evaluer_expression(val) / evaluer_expression(pivot_val) if isinstance(val, (int, float)) and isinstance(pivot_val, (int, float)) else f"{val}/{pivot_val}" for val in tableau[ligne]]
    
    for i in range(len(tableau)):
        if i != ligne:
            facteur = tableau[i][col]
            tableau[i] = [evaluer_expression(val) - evaluer_expression(facteur) * evaluer_expression(tableau[ligne][j]) if isinstance(val, (int, float)) and isinstance(facteur, (int, float)) and isinstance(tableau[ligne][j], (int, float)) else str(val) + " - (" + str(facteur) + "*" + str(tableau[ligne][j]) +")" for j, val in enumerate(tableau[i])]

def simplexe(c, A, b, types_contraintes, maximisation):
    """Résout le problème du simplexe."""
    tableau = tableau_initial_simplexe(c, A, b, types_contraintes, maximisation)

    while True:
        col = colonne_pivot(tableau)
        if col == -1 or all(evaluer_expression(x) >= 0 or isinstance(x, str) for x in tableau[-1][:-1]):
            break

        ligne = ligne_pivot(tableau, col)
        if ligne is None:
            return None
        pivot(tableau, ligne, col)

    solution = [0] * len(c)
    for i in range(len(tableau) - 1):  # Exclure la dernière ligne
        for j in range(len(c)):
            val_ij = evaluer_expression(tableau[i][j])
            if isinstance(val_ij, (int, float)) and abs(val_ij - 1) < 1e-9 and all(abs(evaluer_expression(tableau[k][j])) < 1e-9 for k in range(len(tableau)) if k != i):
                solution[j] = evaluer_expression(tableau[i][-1])
    return tableau, solution, evaluer_expression(tableau[-1][-1])  # Dernière ligne pour Z

def afficher_tableau(tableau, n, m, types_contraintes):
    """Affiche le tableau avec les étiquettes et 'M'."""
    etiquettes = ["Base"] + [f"x{i+1}" for i in range(n)] + [f"s{i+1}" for i in range(m)] + [f"a{i+1}" for i in range(m)] + ["RHS"]
    
    print("\t".join(etiquettes))

    for i, row in enumerate(tableau):
        label = "Z" if i == len(tableau) - 1 else f"Row {i + 1}"
        str_row = [str(val) for val in row]  # Convertit tout en string
        print(label + "\t" + "\t".join(str_row))
    print("\n")

def main():
    """Fonction principale."""
    print("Début du programme")
    c, A, b, types_contraintes, maximisation = obtenir_entrees_utilisateur()

    tableau_initial = tableau_initial_simplexe(c, A, b, types_contraintes, maximisation)
    print("Tableau initial du simplexe :")
    afficher_tableau(tableau_initial, len(c), len(A), types_contraintes)

    tableau_final, solution, valeur_optimale = simplexe(c, A, b, types_contraintes, maximisation)

    if tableau_final is not None:
        print("Tableau final du simplexe :")
        afficher_tableau(tableau_final, len(c), len(A), types_contraintes)
        print("Solution optimale trouvée :")
        print("Valeurs des variables :", solution)
        print("Valeur optimale de Z :", valeur_optimale)
    else:
        print("Le problème est non borné.")

# Exécution du programme
if __name__ == "__main__":
    main()