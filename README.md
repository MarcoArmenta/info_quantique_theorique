# Devoir 4


## Date limite : 2 décembre 2024 à 13h30

Pour ce devoir, créez une branche sur le repositoire. Nommez cette branche avec votre nom. Il s'agit d'un travail individuel, dont la note maximale est de 100 points.
Ce devoir consiste à coder un simulateur de circuits quantiques de Clifford en utilisant le formalisme des stabilisateurs en Python. Suivez ces directives :

* Dans un script nommé *quantumcircuit.py* à la racine du répertoire, vous devez avoir une classe nommée QuantumCircuit qui prend en charge les portes Hadamard, S, CX et n'importe quelle porte de Pauli.

* Dans un script nommé *observables.py* à la racine, vous devez avoir une classe PauliObservable représentant une observable de Pauli. 

* Dans un script nommé *simulator.py*, vous devez avoir une classe nommée GKSimulator qui reçoit un QuantumCircuit et dispose d'une méthode pour mesurer une observable de Pauli donnée. 

* Votre code doit fonctionner en parallèle avec plusieurs cœurs. Je vais exécuter votre code sur 8 cœurs.

* Vous devez utiliser l'environnement virtuel avec le fichier *requirements.txt* fourni dans le repositoire GitHub. Pour ajouter une bibliothèque, vous devez convaincre quatre de vos collègues ; je l'ajouterai alors au fichier des exigences. Si vous n'utilisez pas cette bibliothèque dans votre devoir, je retirerai 10 points à chacun des cinq concernés.
    
* Votre simulateur doit utiliser le formalisme des stabilisateurs pour effectuer la simulation. 
    
* Vous ne pouvez pas utiliser de simulateurs existants ni de kits de développement logiciel (SDK) quantiques.
    
* Vous pouvez utiliser les modèles de langage large (LLM) pour vous aider à coder. Cependant, assurez-vous que le code fonctionne comme prévu. Je recommande *meta.ai*. Ajoutez un commentaire dans votre code pour chaque partie générée par l'IA, précisant son origine. Je vais utiliser un détecteur d'IA. Sans commentaire indiquant l'origine de chaque partie générée par l'IA, 20 points seront retirés de votre note pour chaque occurrence.
    
* Votre code doit être capable de recevoir un fichier JSON contenant plusieurs circuits quantiques à exécuter. Le fichier JSON est composé de listes d'informations pour construire et simuler des circuits. Chaque liste contient, par ordre : Le nombre de qubits, l'observable à mesurer, une list avec les valeurs propres pour lesquelles calculer les probabilités de mesure, et des dictionnaires avec les portes à appliquer. Supposez l'absence de redondances. Exemple :

    [
        7,
        'zzzzzzz',
        ['-+-+-+-','---++++'],
        {
            'x':[6,4,1],
            'cx':[(1,2),(3,2)]
        },
        {
            'h':[1],
            's':[3]
        }
    ],
  
    [
        6,
        'iiizzzz',
        [+-+-,++++],
        {
            'y':[0],
            'z':[1,2,3,4,5],
            'cx':[(1,2),(0,3),(1,4)]
        }
    ]

Vous devriez alors pouvoir créer le QuantumCircuit comme suit :

    l = json.load(file)
    q = QuantumCircuit(l)

Ce devoir sera noté en exécutant 100 circuits de mon choix. Je comparerai les résultats de vos simulations pour chaque circuit aux résultats attendus. Votre note sera la moyenne générale des circuits. Si votre code ne fonctionne pas, vous obtiendrez une note de zéro. Un fichier JSON fictif est disponible *dummy_circuits.json*.

Dans le script *main.py* vous avez une piece de code qui ressembler a:

    l = json.load(file)
    q = QuantumCircuit(l)
    s = GKSimulator()
    r = s.run(q)

Ici, 'r' doit être une liste de dictionnaires contenant les probabilités. Un dictionnaire par circuit. Pour la list
[
        2,
        'zi',
        ['+','-'],
        {
            'h':[0],
            'cx':[(0,1)]
        }
] la list 'r' devrait ressembler à ceci: [
    {
        '+1': 0.5,
        '-1': 0.5
    }
]

# POINTS BONUS
* (15) Effectuez des tests unitaires (unittest) de vos méthodes par rapport à d'autres simulateurs Clifford de votre choix avec 20 circuits aléatoires chacun. 
* (20) Les 3 personnes utilisant moins de mémoire globale dans la méthode s.run(q).
* (20) Les 3 personnes utilisant moins de temps global dans la méthode s.run(q) sur votre ordinateur portable à 8 cœurs.
