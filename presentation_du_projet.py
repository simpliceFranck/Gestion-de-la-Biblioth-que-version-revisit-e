'''
Dans le cadre de la préparation à la certification TOSA en Python, vous allez développer une application de gestion de bibliothèque.

Objectif du projet
Dans le cadre de la préparation à la certification TOSA en Python, vous allez développer une application de gestion de bibliothèque. L'objectif 
est de mettre en pratique les concepts de la Programmation Orientée Objet (POO), de l'optimisation de code, et de développer une application 
utilisable en ligne de commande.

1. Spécifications Générales
L'application doit permettre de :
Gérer une collection de livres (ajout, suppression, mise à jour).
Gérer les utilisateurs de la bibliothèque.
Emprunter et retourner des livres.
Rechercher des livres par différents critères.
Générer des statistiques sur l'utilisation de la bibliothèque (optionnel).

2. Détails des Fonctionnalités

a. Gestion des Livres
Ajouter un livre :
Titre
Auteur
ISBN
Type (Livre Papier, Livre Numérique)
Supprimer un livre :
Par ISBN
Mettre à jour les informations d'un livre :
Titre
Auteur
Type

b. Gestion des Utilisateurs
Ajouter un utilisateur :
Nom
Supprimer un utilisateur :
Par nom

c. Emprunt et Retour
Emprunter un livre :
ISBN du livre
Nom de l'utilisateur
Retourner un livre :
ISBN du livre
Nom de l'utilisateur

d. Recherche et Statistiques
Rechercher des livres :
Par titre, auteur ou ISBN
Lister tous les livres :
Disponibles et empruntés
Générer des statistiques (optionnel) :
Nombre total de livres
Nombre de livres empruntés
Nombre total d'utilisateurs
Livres les plus empruntés

3. Architecture et Conception

a. Programmation Orientée Objet
Classes à implémenter :
Livre (classe de base)
LivrePapier et LivreNumerique (classes dérivées)
Utilisateur
Bibliotheque (Singleton pour gérer l'ensemble de la bibliothèque)

Principes de conception à utiliser :
Encapsulation : Protéger les données des classes.
Héritage : Utiliser des classes dérivées pour différents types de livres.
Polymorphisme : Permettre le traitement des objets de manière uniforme.
Abstraction : Simplifier l'interface pour les utilisateurs de la bibliothèque.

b. Optimisation
Principes d'optimisations à utiliser :
Structures de données : Utiliser des structures de données adaptées pour optimiser les recherches et les mises à jour.
Algorithmes : Comparer différentes méthodes d'implémentation pour trouver les plus efficaces.
Vous pouvez utiliser d'autres principes d'optimisations si vous en connaissez.

4. Utilisation en Ligne de Commande
L'application doit être entièrement utilisable en ligne de commande avec un menu interactif permettant de naviguer entre les différentes 
fonctionnalités. Par exemple :
1. Ajouter un livre
2. Supprimer un livre
3. Rechercher un livre
4. Ajouter un utilisateur
5. Emprunter un livre
6. Retourner un livre
7. Lister les livres
8. Statistiques
9. Quitter

5. Documentation et Tests
Documentation :
Commenter le code pour expliquer les fonctionnalités et les choix techniques.
Fournir un guide utilisateur expliquant comment utiliser l'application.

Tests :
Implémenter des tests unitaires pour vérifier le bon fonctionnement des méthodes.
Effectuer des tests d'intégration pour s'assurer que toutes les parties de l'application fonctionnent bien ensemble.

Critères et livrables
Critères :
- Utilisation de Python 3.7.10 ou plus récent.
- Utilisation appropriée des concepts de la POO.
- Séparation claire des responsabilités.
- Utilisation d'algorithmes et de structures de données efficaces.
- Lisibilité, clarté, et propreté du code.
- Commentaires dans le code.
- Complétude et conformité des fonctionnalités.
- Robustesse et gestion des erreurs.
- Expérience utilisateur en ligne de commande.

Livrables :
- Code source complet de l'application.
- Documentation utilisateur (sous la forme de votre choix).
- Rapport de statistiques sur l'utilisation de la bibliothèque (optionnel).

Quelques idées et suggestions...
Vous pouvez utiliser des libraries comme click, typer ou argparse pour votre interface dans le terminal. Pour typer, vous avez une formation ici 
sur Docstring.

Vous pouvez intégrer une base de données SQL (avec ou sans docker) pour gérer les utilisateurs et les livres afin de
ne pas avoir à les recréer à chaque fois. Une base de donnés SQLite peut très bien faire l'affaire également.

Vous pouvez aussi gérer des types d'utilisateurs différents (admin pour ajouter/supprimer des livres, étudiants pour en
emprunter ou les lister).
'''