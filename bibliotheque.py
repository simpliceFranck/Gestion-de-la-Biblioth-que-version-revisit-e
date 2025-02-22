import logging, pickle, os

from textwrap import dedent
from itertools import chain

# Les constantes
SYMBOLE = "-"
ESPACE = " "

MESSAGE01 = "\nVous n'êtes pas autorisés à effectuer cette opération."
MESSAGE02 = "\nLivre introuvable!"
MESSAGE03 = "\nLe livre que vous retournez n'est pas celui que vous avez emprunté."
MESSAGE04 = "\nCet utilisateur existe déjà dans notre base de données."
MESSAGE05 = "\nImpossible de supprimer cet utilisateur, il est inconnu de notre base de données."
MESSAGE06 = "\nL'utilisateur a été supprimé avec succès."
MESSAGE07 = "\nL'utilisateur a été ajouté avec succès."
MESSAGE08 = "\nLa valeur de l'Isbn doit être une suite de treize chiffres."
MESSAGE09 = "\nLe livre a été ajouté avec succès."
MESSAGE10 = "\nLe livre a été supprimé avec succès."
MESSAGE11 = "\nLe livre existe déjà dans notre base de données."
MESSAGE12 = "\nImpossible de supprimer ce livre, il n'existe pas dans notre base de données !"
MESSAGE13 = "\nOpération impossible, l'ancien livre n'existe pas dans notre base de données !"
MESSAGE14 = "\nLa mise à jour s'est effectuée avec succès."
MESSAGE15 = "\nVotre recherche n'a pas abouti, recherchez par Titre ou par ISBN !\n"
MESSAGE16 = "\nVotre recherche n'a pas abouti, recherchez par Auteur ou par ISBN !\n"
MESSAGE17 = "\nVotre recherche n'a pas abouti, recherchez par Titre ou par Auteur !\n"
MESSAGE18 = "\nL'opération d'emprunt s'est effectuée avec succès."
MESSAGE19 = "\nLe livre que vous voulez emprunter n'est pas disponible."
MESSAGE20 = "\nImpossible d'emprunter ce livre, il n'existe pas dans notre base de données !"
MESSAGE21 = "\nL'opération ne peut aboutir, vous n'êtes pas un abonné."
MESSAGE22 = "\nOpération impossible, le nom ne correspond à aucun nom d'emprunteur connu !"
MESSAGE23 = "\nLa restitution s'est déroulée avec succès."
MESSAGE24 = "\n Une erreur s'est produite lors de la sauvergade de données utilisateurs."
MESSAGE25 = "\n Une erreur s'est produite lors de la sauvergade de données (Livres Disponibles)."
MESSAGE26 = "\n Une erreur s'est produite lors de la sauvergade de données (Livres Empruntés)."
MESSAGE27 = "\n Une erreur s'est produite lors de la restitution de données utilisateurs."
MESSAGE28 = "\n Une erreur s'est produite lors de la restitution de données (Livres Disponibles)."
MESSAGE29 = "\n Une erreur s'est produite lors de la restitution de données (Livres Empruntés)."


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


# Classe exception personnalisée
class MonError(Exception):
    ...


class Livre:

    def __init__(self, titre, auteur, isbn) -> None:
        self.__titre = titre
        self.__auteur = auteur
        self.__isbn = isbn
    
    def gettitre(self):
        return self.__titre
    
    def getauteur(self):
        return self.__auteur
    
    def getisbn(self):
        return self.__isbn
    
    def enregistrer_livre(self):
        biblio.get_livres_disponibles()[self.__isbn] = self
   
    def retirer_livre(self):
        del biblio.get_livres_disponibles()[self.__isbn]
    
    
    def description(self):
        # Terminez la première ligne par \ pour éviter la ligne vide !
        print(dedent(f"""\
            Titre  : {self.__titre}
            Auteur : {self.__auteur}
            Isbn   : {self.__isbn}"""))


    def emprunter(self, nom):
        if not biblio.get_livres_empruntes().get(nom):
            biblio.get_livres_empruntes()[nom] = [self]
            self.retirer_livre()
        else:
            biblio.get_livres_empruntes()[nom].append(self)
            self.retirer_livre()

    
    def restituer(self, nom):
        if len(biblio.get_livres_empruntes()[nom]) > 1:
            biblio.get_livres_empruntes()[nom].remove(self)
        else:
            del biblio.get_livres_empruntes()[nom]
        
        self.enregistrer_livre()

    
    def mise_a_jour_livre(self, nouveau_titre, nouveau_auteur):
        self.__titre = nouveau_titre
        self.__auteur = nouveau_auteur



class LivrePapier(Livre):

    def __init__(self, titre, auteur, ibsn, type='Livre Papier') -> None:
        super().__init__(titre, auteur, ibsn)
        self.__type = type
    
    def gettype(self):
        return self.__type
    
    def description(self):
        super().description()
        print(f"Type   : {self.__type}")
    
    def mise_a_jour_livre(self, nouveau_titre, nouveau_auteur, nouveau_type):
        super().mise_a_jour_livre(nouveau_titre, nouveau_auteur)
        self.__type = nouveau_type



class LivreNumerique(Livre):

    def __init__(self, titre, auteur, ibsn, type='Livre Numérique') -> None:
        super().__init__(titre, auteur, ibsn)
        self.__type = type
    
    def gettype(self):
        return self.__type
    
    def description(self):
        super().description()
        print(f"Type   : {self.__type}")
    
    def mise_a_jour_livre(self, nouveau_titre, nouveau_auteur, nouveau_type):
        super().mise_a_jour_livre(nouveau_titre, nouveau_auteur)
        self.__type = nouveau_type



class Utilisateur:

    def __init__(self, nom, statut) -> None:
        self.__nom = nom
        self.__statut = statut
    
    def getnom(self):
        return self.__nom
    
    def getstatut(self):
        return self.__statut
    

    def ajouter_utilisateur(self, nom, statut):
        if self.__statut != 'admin':
            raise MonError(MESSAGE01)
        
        if list(filter(lambda x: x.getnom() == nom, biblio.get_utilisateurs().values())):
            print(biblio.get_utilisateurs())
            print()
            LOGGER.error(MESSAGE04)
        else:
            utilisateur = Utilisateur(nom, statut)
            biblio.get_utilisateurs()[nom] = utilisateur
            print(biblio.get_utilisateurs())
            print()
            LOGGER.info(MESSAGE07)
    

    def supprimer_utilisateur(self, nom):
        if self.__statut != 'admin':
            raise MonError(MESSAGE01)
        
        if list(filter(lambda x: x.getnom() == nom, biblio.get_utilisateurs().values())):
            utilisateur = list(filter(lambda x: x.getnom() == nom, biblio.get_utilisateurs().values()))[0]
            del biblio.get_utilisateurs()[utilisateur.getnom()]
            print(biblio.get_utilisateurs())
            print()
            LOGGER.info(MESSAGE06)
        else:
            print(biblio.get_utilisateurs())
            print()
            LOGGER.error(MESSAGE05)
    

    def ajouter_livre(self, titre, auteur, isbn):
        if self.__statut != 'admin':
            raise MonError(MESSAGE01)

        type = input("Nouveau Type (tapez 1 pour 'Livre Papier' ou 2 pour 'Livre Numérique') : ")
        if type == '1':
            livre = LivrePapier(titre, auteur, isbn)
        elif type == '2':
            livre = LivreNumerique(titre, auteur, isbn)

        for liv in biblio.get_livres_disponibles().values():
            if all((liv.gettitre() == titre, liv.getauteur() == auteur, liv.getisbn() == isbn)):
                print(biblio.get_livres_disponibles())
                print()
                LOGGER.error(MESSAGE11)
                break
        else:
            livre.enregistrer_livre()
            print(biblio.get_livres_disponibles())
            print()
            LOGGER.info(MESSAGE09)
    
    def supprimer_livre(self, isbn):
        if self.__statut != 'admin':
            raise MonError(MESSAGE01)
        
        if list(filter(lambda x: x.getisbn() == isbn, biblio.get_livres_disponibles().values())):
            livre = list(filter(lambda x: x.getisbn() == isbn, biblio.get_livres_disponibles().values()))[0]
            livre.retirer_livre()
            print(biblio.get_livres_disponibles())
            print()
            LOGGER.info(MESSAGE10)
        else:
            print(biblio.get_livres_disponibles())
            print()
            LOGGER.error(MESSAGE12)
    
    def mettre_a_jour_livre(self, ancien_titre, ancien_auteur, ancien_type, nouveau_titre, nouveau_auteur, nouveau_type):
        
        if self.__statut != 'admin':
            raise MonError(MESSAGE01)
        
        if ancien_type == nouveau_type:
            if list(filter(lambda x: x.gettitre() == ancien_titre, biblio.get_livres_disponibles().values())):
                ancien_livre = list(filter(lambda x: x.gettitre() == ancien_titre, biblio.get_livres_disponibles().values()))[0]
                ancien_livre.mise_a_jour_livre(nouveau_titre, nouveau_auteur, nouveau_type)
                print(biblio.get_livres_disponibles())
                print()
                LOGGER.info(MESSAGE14)
            else:
                print(biblio.get_livres_disponibles)
                print()
                LOGGER.error(MESSAGE13)

        elif nouveau_type == 'Livre Papier':
            if list(filter(lambda x: x.gettitre() == ancien_titre, biblio.get_livres_disponibles().values())):
                ancien_livre = list(filter(lambda x: x.gettitre() == ancien_titre, biblio.get_livres_disponibles().values()))[0]
                nouveau_livre = LivrePapier(nouveau_titre, nouveau_auteur, ancien_livre.getisbn())
                ancien_livre.retirer_livre()
                nouveau_livre.enregistrer_livre()
                print()
                LOGGER.info(MESSAGE14)
            else:
                print(biblio.get_livres_disponibles)
                print()
                LOGGER.error(MESSAGE13)
        elif nouveau_type == 'Livre Numérique':
            if list(filter(lambda x: x.gettitre() == ancien_titre, biblio.get_livres_disponibles().values())):
                ancien_livre = list(filter(lambda x: x.gettitre() == ancien_titre, biblio.get_livres_disponibles().values()))[0]
                nouveau_livre = LivreNumerique(nouveau_titre, nouveau_auteur, ancien_livre.getisbn())
                ancien_livre.retirer_livre()
                nouveau_livre.enregistrer_livre()
                print()
                LOGGER.info(MESSAGE14)
            else:
                print(biblio.get_livres_disponibles)
                print()
                LOGGER.error(MESSAGE13)
    
    def rechercher_livre(self):
        test = False

        while not test:
            print("Vous pouvez rechercher un livre par :")
            print("Auteur (tapez 1)")
            print("Titre (tapez 2)")
            print("ISBN (tapez 3)")
            print("Sortir (tapez 4)\n")

            choix = input("Votre choix : ")
            # On recherche par le nom d'auteur.
            if choix == '1':
                auteur = input("\nAuteur du livre : ").lower().title()
                for livre in biblio.get_livres_disponibles().values():
                    if livre.getauteur() == auteur: 
                        livre.description()
                        test = True
                        break
                else:
                    print()
                    LOGGER.info(MESSAGE15)
            # On recherche par le titre du livre.            
            elif choix == '2':
                titre = input("\nTitre du livre : ").lower().title()
                for livre in biblio.get_livres_disponibles().values():
                    if livre.gettitre() == titre:
                        livre.description()
                        test = True
                        break
                else:
                    print()
                    LOGGER.info(MESSAGE16)
            # On recherche par l'isbn du livre.
            elif choix == '3':
                isbn = input("\nISBN du livre : ")
                for livre in biblio.get_livres_disponibles().values():
                    if livre.getisbn() == isbn:
                        livre.description()
                        test = True
                        break
                else:
                    print()
                    LOGGER.info(MESSAGE17)
            # On sort de la boucle while.
            elif choix == '4':
                break

    def emprunter_livre(self, isbn, nom):
        if self.__statut != 'admin':
            raise MonError(MESSAGE01)
            
        if nom not in biblio.get_utilisateurs():
            raise MonError(MESSAGE21)
        
        for liv in biblio.get_livres_disponibles().values():
            if liv.getisbn() == isbn:
                liv.emprunter(nom)
                print(biblio.get_livres_disponibles())
                print(biblio.get_livres_empruntes())
                print()
                LOGGER.info(MESSAGE18 )
                break
        else:
            for liv in chain(*(biblio.get_livres_empruntes().values())):
                if liv.getisbn() == isbn:
                    print()
                    LOGGER.info(MESSAGE19)
                    break
            else:
                print()
                LOGGER.error(MESSAGE20)

    def retourner_livre(self, isbn, nom):
        if self.__statut != 'admin':
            raise MonError(MESSAGE01)
        
        if nom not in biblio.get_utilisateurs():
            raise MonError(MESSAGE21)
        
        if nom not in biblio.get_livres_empruntes():
            raise MonError(MESSAGE22)
        
        for liv in biblio.get_livres_empruntes().get(nom):
            if liv.getisbn() == isbn:
                liv.restituer(nom)
                print(biblio.get_livres_empruntes())
                print(biblio.get_livres_disponibles())
                print()
                LOGGER.info(MESSAGE23)
                break
        else: 
            print(biblio.get_livres_empruntes())
            print(biblio.get_livres_disponibles())
            print()
            LOGGER.error(MESSAGE03)
    
    def lister_livres(self):
        print("\nLivres disponibles:")
        for ind, livre in enumerate(biblio.get_livres_disponibles().values()):
            print(f"{ind + 1}°/")
            livre.description()

        print("\nLivres empruntés :")
        for ind, livre in enumerate(chain(*(biblio.get_livres_empruntes().values()))):
            print(f"{ind +1}°/")
            livre.description()


class Bibliotheque:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Bibliotheque, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self) -> None:
        self.__nom = 'Bibliothèque François Villon'
        self.__adresse = '81, boulevard de la Villette, 75010 Paris'
        self.__utilisateurs = {}
        self.__livres_disponibles = {}
        self.__livres_empruntes = {}
    
    def get_utilisateurs(self):
        return self.__utilisateurs

    def get_livres_disponibles(self):
        return self.__livres_disponibles
    
    def get_livres_empruntes(self):
        return self.__livres_empruntes

    
    def statistiques(self):
        print(dedent(f"""\
                        Total utilisateurs       : {len(self.__utilisateurs)} 
                        Total livres disponibles : {len(self.__livres_disponibles)}
                        Total livres empruntés   : {len(list(chain(*(self.__livres_empruntes.values()))))}"""))
        
    
    def __sauvegarder_utilisateurs(self):
        try:
            with open('utilisateurs_data.pickle', 'wb') as f:
                pickle.dump(self.__utilisateurs, f)
        except:
            LOGGER.error(MESSAGE24)
    
    def __restituer_utilisateurs(self):
        try:
            if os.path.exists('utilisateurs_data.pickle'):
                with open('utilisateurs_data.pickle', 'rb') as f:
                    self.__utilisateurs = pickle.load(f)
        except:
            LOGGER.error(MESSAGE27)


    def ___sauvegarder_livres_disponibles(self):
        
        try:
            with open('livres_disponibles_data.pickle', 'wb') as f:
                pickle.dump(self.__livres_disponibles, f)
        except:
            LOGGER.error(MESSAGE25)
    

    def __restituer_livres_disponibles(self):
        try:
            if os.path.exists('utilisateurs_data.pickle'):
                with open('livres_disponibles_data.pickle', 'rb') as f:
                        self.__livres_disponibles = pickle.load(f)
        except:
            LOGGER.error(MESSAGE28)
    

    def __sauvegarder_livres_emprunter(self):
        
        try:
            with open('livres_empruntes_data.pickle', 'wb') as f:
                pickle.dump(self.__livres_empruntes, f)
        except:
            LOGGER.error(MESSAGE26)
    
    
    def __restituer_livres_empruntes(self):
        try:
            if os.path.exists('utilisateurs_data.pickle'):
                with open('livres_empruntes_data.pickle', 'rb') as f:
                        self.__livres_empruntes = pickle.load(f)
        except:
            LOGGER.error(MESSAGE29)
    
    def se_connecter(self, nom):
        self.__restituer_utilisateurs()
        self.__restituer_livres_disponibles()
        self.__restituer_livres_empruntes()

        if not nom in self.__utilisateurs:
            raise MonError(MESSAGE21)
            
        usager = self.__utilisateurs[nom]
        print(self.__utilisateurs)
        print(self.__livres_disponibles)
        print(self.__livres_empruntes)
        return usager
    

    def se_deconnecter(self):
        self.__sauvegarder_utilisateurs()
        self.___sauvegarder_livres_disponibles()
        self.__sauvegarder_livres_emprunter()
        
        

class MenuInteratif:

    def __contrôler_la_validite_de_isbn(self):

        while True:
            isbn = input("Isbn : ")
            if isbn.isdigit() and len(isbn) == 13:
                break
            LOGGER.error(MESSAGE08)

        return isbn
    

    def __demander_titre_et_auteur(self):

        titre = input("Nouveau Titre : ").lower().title()
        auteur = input("Nouveau Auteur : ").lower().title()

        return titre, auteur


    def __demander_isbn_et_nom(self):

        isbn = self.__contrôler_la_validite_de_isbn()
        nom = input("Nom de l'emprunteur : ").lower().title()

        return isbn, nom   

    def boucle_de_saisie(self):

        print(F"\n{SYMBOLE*29} CONNEXION {SYMBOLE*29}")

        while True:
            choix = input("Pour se connecter (tapez 0) : ")
            if choix == '0':
                print()
                nom = input('Votre nom : ').lower().capitalize()
                employe = biblio.se_connecter(nom)
                break

        while True:
            print(dedent(f"""
                         {SYMBOLE*22}MENU ITERATIF{SYMBOLE*22}
                         Ajouter un utilisateur{ESPACE*25}: tapez 1
                         Supprimer un utilisateur{ESPACE*23}: tapez 2
                         Ajouter un livre{ESPACE*31}: tapez 3
                         Supprimer un livre{ESPACE*29}: tapez 4
                         Rechercher un livre{ESPACE*28}: tapez 5                        
                         Emprunter un livre{ESPACE*29}: tapez 6
                         Retourner un livre{ESPACE*29}: tapez 7
                         Lister les livres{ESPACE*30}: tapez 8
                         Mettre à jour des informations d'un livre{ESPACE*5} : tapez 9
                         Statistiques{ESPACE*35}: tapez 10                        
                         Quitter{ESPACE*40}: tapez 11\n"""))
            
            choix = input('Votre choix : ')

            if choix == '1':
                print(f"\n{SYMBOLE*17}AJOUT D'UN UTILISATEUR{SYMBOLE*17}")
                nom = input("Nom : ").lower().capitalize()
                statut = input("Statut : ").lower().capitalize()
                employe.ajouter_utilisateur(nom, statut)

            elif choix == '2':
                print(f"\n{SYMBOLE*14}SUPPRESSION D'UN UTILISATEUR{SYMBOLE*14}")
                nom = input("Nom : ").lower().capitalize()
                employe.supprimer_utilisateur(nom)

            elif choix == '3':
                print(f"\n{SYMBOLE*20}AJOUT D'UN LIVRE{SYMBOLE*20}")

                titre, auteur = self.__demander_titre_et_auteur()

                isbn = self.__contrôler_la_validite_de_isbn()

                employe.ajouter_livre(titre, auteur, isbn)

            elif choix == '4':
                print(f"\n{SYMBOLE*17}SUPPRESSION D'UN LIVRE{SYMBOLE*17}")
                isbn = self.__contrôler_la_validite_de_isbn()
                employe.supprimer_livre(isbn)

            elif choix == '5':
                print(f"\n{SYMBOLE*18}RECHERCHE D'UN LIVRE{SYMBOLE*18}")
                employe.rechercher_livre()

            elif choix == '6':
                print(f"\n{SYMBOLE*19}EMPRUNT D'UN LIVRE{SYMBOLE*19}")
                isbn, nom = self.__demander_isbn_et_nom()
                employe.emprunter_livre(isbn, nom)

            elif choix == '7':
                print(f"\n{SYMBOLE*17}RESTITUTION D'UN LIVRE{SYMBOLE*17}")
                isbn, nom = self.__demander_isbn_et_nom()
                employe.retourner_livre(isbn, nom)

            elif choix == '8':
                employe.lister_livres()
            
            elif choix == '9':
                print(f"\n{SYMBOLE*17}MISE A JOUR D'UN LIVRE{SYMBOLE*17}")
                nouveau_titre, nouveau_auteur = self.__demander_titre_et_auteur()
                type1 = input("Nouveau Type (tapez 1 pour 'Livre Papier' ou 2 pour 'Livre Numérique') : ")
                if type1 == '1':
                    nouveau_type = 'Livre Papier'
                elif type1 == '2':
                    nouveau_type = 'Livre Numérique'
                
                ancien_titre = input("Ancien Titre : ").lower().title()
                ancien_auteur = input("Ancien Auteur : ").lower().title()
                type2 = input("Ancien Type (tapez 1 pour 'Livre Papier' ou 2 pour 'Livre Numérique') : ")
                if type2 == '1':
                    ancien_type = 'Livre Papier'
                elif type2 == '2':
                    ancien_type = 'Livre Numérique'

                employe.mettre_a_jour_livre(ancien_titre, ancien_auteur, ancien_type, nouveau_titre, nouveau_auteur, nouveau_type)

            elif choix == '10':
                print(f"\n{SYMBOLE*20}LES STATISTIQUES{SYMBOLE*20}")
                biblio.statistiques()
            
            elif choix == '11':
                biblio.se_deconnecter()
                break       


if __name__ == '__main__':
    biblio = Bibliotheque()
    employe = Utilisateur('Franck', 'admin')
    biblio.get_utilisateurs()['Franck'] = employe
    menu = MenuInteratif()
    menu.boucle_de_saisie()