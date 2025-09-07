# Architecture requise :
# musiques.py
# musiques_enregistrées.py (crée automatiquement s'il n'existe pas, sert de mémoire pour les musiques classées)
# accueil.png
# Musiques/ (dossier)
#     -Musique1.mp3
#     -Musique2.mp3
#     -Musique3.mp3
#     -Musique4.mp3
#     -Musique5.mp3
#     ....


#Lecteur de musique pondéré
# Contrôles:
# - Fleche gauche : Jouer une nouvelle musique
# - espcace Fleche droite : Pause/Play de la musique actuelle
# - fleche gauche : Musique précédente
# - C : Reclassifier la musique actuelle
# - C : Classer les nouveaux fichiers (si disponibles)
# - S : Ignorer les nouveaux fichiers (si disponibles)
# - ÉCHAP: Quitter le programme
# - Clic sur X: Fermer la fenêtre
# - fleche haut : augmenter la note de 1
# - fleche bas : diminuer la note de 1

# En mode classification/reclassification:
# - 0-9: Noter directement (0=très mauvais, 9=excellent)
# - ÉCHAP: Annuler/Passer

from random import randint
import pygame
import os
import json
try:
    from musiques_enregistrées import MUSIQUES_ENREGISTREES
except ImportError:
    # Créer le fichier musiques_enregistrées.py s'il n'existe pas
    print("Fichier musiques_enregistrées.py non trouvé, création automatique...")
    
    # Structure par défaut des musiques enregistrées
    MUSIQUES_ENREGISTREES = {
        0: [],
        (1, 2): [],
        (3, 4, 5): [],
        (6, 7, 8, 9): [],
        (10, 11, 12, 13, 14): [],
        (15, 16, 17, 18, 19, 20): [],
        (21, 22, 23, 24, 25, 26, 27): [],
        (28, 29, 30, 31, 32, 33, 34, 35): [],
        (36, 37, 38, 39, 40, 41, 42, 43, 44): [],
        (45, 46, 47, 48, 49, 50, 51, 52, 53, 54): [],
    }
    
    # Créer le fichier
    with open("musiques_enregistrées.py", "w", encoding="utf-8") as f:
        f.write("MUSIQUES_ENREGISTREES = {\n")
        for key, value in MUSIQUES_ENREGISTREES.items():
            if isinstance(key, tuple):
                f.write(f"    {key}: [\n")
            else:
                f.write(f"    {key}: [\n")
            for item in value:
                f.write(f'        "{item}",\n')
            f.write("    ],\n")
        f.write("}\n")
    
    print("Fichier musiques_enregistrées.py créé avec succès!")
except Exception as e:
    print(f"Erreur lors de la création du fichier musiques_enregistrées.py: {e}")


    
# Initialisation de pygame
try:
    pygame.init()
    print("Pygame initialisé avec succès!")
except Exception as e:
    print(f"Erreur lors de l'initialisation de pygame: {e}")
    exit(1)

# Configuration de la fenêtre
try:
    window_resolution = (740, 580)
    screen = pygame.display.set_mode(window_resolution)
    pygame.display.set_caption("Lecteur de Musique pondéré")
    print(f"Fenêtre créée: {window_resolution}")
    
    # Charger l'image d'accueil
    try:
        image = pygame.image.load("accueil.png").convert()
        print("Image d'accueil chargée avec succès")
    except Exception as e:
        print(f"Erreur lors du chargement de l'image: {e}")
        # Créer une image par défaut si l'image n'est pas trouvée
        image = pygame.Surface(window_resolution)
        image.fill((50, 50, 100))  # Fond bleu foncé
    
    # Créer la police
    police = pygame.font.Font(None, 36)
    print("Police créée avec succès")
    
except Exception as e:
    print(f"Erreur lors de la création de la fenêtre: {e}")
    exit(1)

# Dictionnaire des musiques dans le répertoire Musiques
MUSIQUES_CLASSEES = {
    0: [],
    (1, 2):[],
    (3, 4, 5): [],
    (6, 7, 8, 9):[],
    (10, 11, 12, 13, 14): [],
    (15, 16, 17, 18, 19, 20): [],
    (21, 22, 23, 24, 25, 26, 27): [],
    (28, 29, 30, 31, 32, 33, 34, 35):[],
    (36, 37, 38, 39, 40, 41, 42, 43, 44): [],
    (45, 46, 47, 48, 49, 50, 51, 52, 53, 54): [],
}


# Variables globales
launched = True
texte = None  # Variable pour afficher le texte à l'écran
texte_ligne2 = None  # Variable pour afficher la deuxième ligne de texte
musique_prec = None  # Variable pour stocker la musique précédente
fichier_actuel = None  # Variable pour stocker le chemin du fichier actuel
musique_en_cours = None
note_musique = None
is_paused = False  # Variable pour gérer la pause/play
message_temporaire = None  # Variable pour les messages temporaires
message_temporaire_ligne2 = None  # Variable pour la deuxième ligne des messages temporaires
temps_message_temporaire = 0  # Temps d'affichage du message temporaire
# Variables pour la classification
nouveaux_fichiers = []  # Liste des nouveaux fichiers à classer
fichier_en_cours_de_classification = None  # Fichier actuellement en cours de classification
en_mode_classification = False  # Indique si on est en mode classification
en_mode_reclassification = False  # Indique si on est en mode reclassification
ancienne_categorie = None  # Ancienne catégorie de la musique en cours de reclassification


def synchroniser_musiques_disponibles():
    """Synchronise MUSIQUES_CLASSEES avec seulement les fichiers qui existent réellement"""
    global MUSIQUES_CLASSEES, MUSIQUES_ENREGISTREES
    
    fichiers_manquants = []
    for note, fichiers in MUSIQUES_ENREGISTREES.items():
        fichiers_disponibles = []
        for fichier in fichiers:
            if os.path.exists(fichier):
                fichiers_disponibles.append(fichier)
            else:
                fichiers_manquants.append(fichier)
        MUSIQUES_CLASSEES[note] = fichiers_disponibles
    
    if fichiers_manquants:
        print(f"Note: {len(fichiers_manquants)} fichiers manquants détectés (conservés dans l'historique)")
        for fichier in fichiers_manquants:
            print(f"  - {fichier}")
        print("Ces fichiers restent dans l'historique mais ne seront pas joués")

def parcourir_repertoire_musiques():
    """Parcourt le répertoire Musiques et classe les fichiers"""
    global MUSIQUES_CLASSEES, MUSIQUES_ENREGISTREES
    
    # Synchroniser avec les fichiers disponibles
    synchroniser_musiques_disponibles()
    
    # Vérifier si le dossier Musiques existe, le créer s'il n'existe pas
    if not os.path.exists("Musiques"):
        print("Le dossier Musiques n'existe pas, création automatique...")
        try:
            os.makedirs("Musiques")
            print("Dossier Musiques créé avec succès!")
            print("Ajoutez vos fichiers MP3 dans le dossier Musiques/ et relancez le programme.")
            return []
        except Exception as e:
            print(f"Erreur lors de la création du dossier Musiques: {e}")
            return []
    
    # Lister tous les fichiers .mp3 dans le dossier
    fichiers_mp3 = []
    for fichier in os.listdir("Musiques"):
        if fichier.lower().endswith('.mp3'):
            fichiers_mp3.append(f"Musiques/{fichier}")
    
    print(f"Trouvé {len(fichiers_mp3)} fichiers MP3 dans le dossier Musiques")
    
    # Vérifier si les fichiers sont déjà classés
    fichiers_classes = []
    for fichiers_cat in MUSIQUES_ENREGISTREES.values():
        fichiers_classes.extend(fichiers_cat)
    
    # Trouver les nouveaux fichiers non classés
    nouveaux_fichiers = [f for f in fichiers_mp3 if f not in fichiers_classes]
    
    if nouveaux_fichiers:
        print(f"Trouvé {len(nouveaux_fichiers)} nouveaux fichiers non classés")
        print("Appuyez sur 'C' pour classer les nouveaux fichiers ou 'S' pour ignorer et commencer directement")

        # Attendre la décision de l'utilisateur
        return nouveaux_fichiers
    else:
        print("Tous les fichiers sont déjà classés!")
        # Copier les fichiers classés vers MUSIQUES_CLASSEES
        for note, fichiers in MUSIQUES_ENREGISTREES.items():
            for fichier in fichiers:
                if os.path.exists(fichier):
                    MUSIQUES_CLASSEES[note].append(fichier)
                else:
                    pass
        return []

def synchroniser_musiques_classees():
    """Synchronise MUSIQUES_CLASSEES avec MUSIQUES_ENREGISTREES"""
    global MUSIQUES_CLASSEES, MUSIQUES_ENREGISTREES
    
    # Copier tous les fichiers classés vers MUSIQUES_CLASSEES
    for note, fichiers in MUSIQUES_ENREGISTREES.items():
        for fichier in fichiers:
            if os.path.exists(fichier):
                MUSIQUES_CLASSEES[note].append(fichier)
            else:
                pass
    
    print("Synchronisation des musiques terminée")

def ignorer_nouveaux_fichiers():
    """Ignore les nouveaux fichiers et utilise seulement les musiques déjà enregistrées"""
    global MUSIQUES_CLASSEES, MUSIQUES_ENREGISTREES
    
    # Synchroniser les dictionnaires
    synchroniser_musiques_classees()
    
    print("Utilisation des musiques déjà enregistrées uniquement")

def afficher_texte_multiligne(ligne1, ligne2=None, couleur1=(255, 255, 255), couleur2=(255, 255, 255), temporaire=False, duree=2000):
    """Affiche du texte sur une ou deux lignes"""
    global texte, texte_ligne2, message_temporaire, message_temporaire_ligne2, temps_message_temporaire
    
    if temporaire:
        # Message temporaire
        message_temporaire = police.render(ligne1, True, couleur1)
        if ligne2:
            message_temporaire_ligne2 = police.render(ligne2, True, couleur2)
        else:
            message_temporaire_ligne2 = None
        temps_message_temporaire = pygame.time.get_ticks() + duree
    else:
        # Message permanent
        texte = police.render(ligne1, True, couleur1)
        if ligne2:
            texte_ligne2 = police.render(ligne2, True, couleur2)
        else:
            texte_ligne2 = None
        # Effacer les messages temporaires
        message_temporaire = None
        message_temporaire_ligne2 = None

def commencer_classification():
    """Commence la classification des nouveaux fichiers"""
    global nouveaux_fichiers, fichier_en_cours_de_classification, en_mode_classification, musique_en_cours, texte
    
    if nouveaux_fichiers:
        en_mode_classification = True
        fichier_en_cours_de_classification = nouveaux_fichiers[0]
        
        # Jouer le fichier à classer
        try:
            if musique_en_cours:
                musique_en_cours.stop()
            musique_en_cours = pygame.mixer.Sound(fichier_en_cours_de_classification)
            musique_en_cours.play()
            
            nom_fichier = fichier_en_cours_de_classification.split("/")[-1]
            if len(nom_fichier) > 30:
                nom_fichier = nom_fichier[:30] + "..."
            afficher_texte_multiligne(f"Classification: {nom_fichier}", "Appuyez sur 0-9 pour noter", (25, 100, 255), (25, 100, 255))
            print(f"Classification: {nom_fichier}")
        except Exception as e:
            print(f"Erreur lors du chargement de {fichier_en_cours_de_classification}: {e}")
            passer_fichier_suivant()

def classer_fichier_actuel(note):
    """Classe le fichier actuellement en cours de classification"""
    global nouveaux_fichiers, fichier_en_cours_de_classification, en_mode_classification
    
    if fichier_en_cours_de_classification:
        ajouter_fichier_aux_categories(fichier_en_cours_de_classification, note)
        print(f"Fichier {fichier_en_cours_de_classification.split('/')[-1]} classé avec la note {note}")
        
        # Passer au fichier suivant
        passer_fichier_suivant()

def passer_fichier_suivant():
    """Passe au fichier suivant dans la classification"""
    global nouveaux_fichiers, fichier_en_cours_de_classification, en_mode_classification, musique_en_cours, texte
    
    if nouveaux_fichiers:
        nouveaux_fichiers.pop(0)  # Retirer le fichier traité
        
        if nouveaux_fichiers:
            # Il y a encore des fichiers à classer
            fichier_en_cours_de_classification = nouveaux_fichiers[0]
            try:
                if musique_en_cours:
                    musique_en_cours.stop()
                musique_en_cours = pygame.mixer.Sound(fichier_en_cours_de_classification)
                musique_en_cours.play()
                
                nom_fichier = fichier_en_cours_de_classification.split("/")[-1]
                if len(nom_fichier) > 30:
                    nom_fichier = nom_fichier[:30] + "..."
                afficher_texte_multiligne(f"Classification: {nom_fichier}", "Appuyez sur 0-9 pour noter", (25, 100, 255), (20, 100, 255))
                print(f"Classification: {nom_fichier}")
            except Exception as e:
                print(f"Erreur lors du chargement de {fichier_en_cours_de_classification}: {e}")
                passer_fichier_suivant()
        else:
            # Fin de la classification
            en_mode_classification = False
            fichier_en_cours_de_classification = None
            # Synchroniser les dictionnaires après la classification
            synchroniser_musiques_classees()
            afficher_texte_multiligne("Classification terminée!", "Appuyez sur la flèche droite pour jouer", (0, 255, 0), (0, 255, 0))
            print("Classification terminée!")
    else:
        # Fin de la classification
        en_mode_classification = False
        fichier_en_cours_de_classification = None
        # Synchroniser les dictionnaires après la classification
        synchroniser_musiques_classees()
        afficher_texte_multiligne("Classification terminée!", "Appuyez sur la flèche droite pour jouer", (0, 255, 0), (0, 255, 0))
        print("Classification terminée!")

def ajouter_fichier_aux_categories(fichier, note):
    """Ajoute un fichier aux catégories appropriées basées sur sa note"""
    global MUSIQUES_CLASSEES, MUSIQUES_ENREGISTREES
    print("note", note)
    # Déterminer la catégorie basée sur la note (0-9)
    if note == 0:
        categorie = 0
    elif note == 1:
        categorie = (1, 2)
    elif note == 2:
        categorie = (3, 4, 5)
    elif note == 3:
        categorie = (6, 7, 8, 9)
    elif note == 4:
        categorie = (10, 11, 12, 13, 14)
    elif note == 5:
        categorie = (15, 16, 17, 18, 19, 20)
    elif note == 6:
        categorie = (21, 22, 23, 24, 25, 26, 27)
    elif note == 7:
        categorie = (28, 29, 30, 31, 32, 33, 34, 35)
    elif note == 8:
        categorie = (36, 37, 38, 39, 40, 41, 42, 43, 44)
    elif note == 9:
        categorie = (45, 46, 47, 48, 49, 50, 51, 52, 53, 54)
    
    # Ajouter aux deux dictionnaires
    try:
        MUSIQUES_ENREGISTREES[categorie].append(fichier)
        MUSIQUES_CLASSEES[categorie].append(fichier)
        
        # Sauvegarder le dictionnaire complet dans le fichier
        with open("musiques_enregistrées.py", "w", encoding="utf-8") as f:
            f.write("MUSIQUES_ENREGISTREES = {\n")
            for key, value in MUSIQUES_ENREGISTREES.items():
                if isinstance(key, tuple):
                    f.write(f"    {key}: [\n")
                else:
                    f.write(f"    {key}: [\n")
                for item in value:
                    f.write(f'        "{item}",\n')
                f.write("    ],\n")
            f.write("}\n")
        
        print(f"Fichier {fichier} ajouté à la catégorie {categorie} et sauvegardé")
    except Exception as e:
        print(f"Erreur lors de l'insertion: {e}")

def jouer_musique_aleatoire():
    """Joue une musique aléatoire basée sur note_musique"""
    global musique_en_cours, texte, musique_prec, fichier_actuel, is_paused, note_musique
    
    # Arrêter la musique en cours si elle existe
    if musique_en_cours:
        try:
            musique_en_cours.stop()
        except:
            pass
    
    # Réinitialiser l'état de pause
    is_paused = False
    
    # Vérifier s'il y a des musiques disponibles
    total_musiques = sum(len(fichiers) for fichiers in MUSIQUES_CLASSEES.values())
    if total_musiques == 0:
        print("Aucune musique disponible dans la base de données")
        afficher_texte_multiligne("Aucune musique disponible", "Ajoutez des fichiers MP3 dans le dossier Musiques/", (255, 0, 0), (255, 0, 0))
        return
    
    # Essayer plusieurs fois de trouver une musique
    for tentative in range(10):  # Maximum 10 tentatives
        note_musique = randint(0, 54)

        # Trouver la note correspondante
        fichiers = None
        for note, fichiers_cat in MUSIQUES_CLASSEES.items():
            if isinstance(note, tuple):
                if note_musique in note:
                    fichiers = fichiers_cat
                    break
            elif note_musique == note:
                fichiers = fichiers_cat
                break
        
        if fichiers and len(fichiers) > 0:
            break
    
    if not fichiers or len(fichiers) == 0:
        print(f"Aucune musique trouvée pour une note de {note_musique}")
        afficher_texte_multiligne(f"Aucune musique trouvée pour une note de {note_musique}", "Essayez une autre note", (255, 0, 0), (255, 0, 0))
        return

    # Choisir et jouer un fichier aléatoire
    fichier_choisi = randint(0, len(fichiers) - 1)
    fichier = fichiers[fichier_choisi]

    # Vérifier que le fichier existe avant de l'utiliser
    if not os.path.exists(fichier):
        print(f"Fichier manquant: {fichier} (conservé dans l'historique)")
        # Ne pas supprimer de la base de données, juste réessayer
        jouer_musique_aleatoire()
        return 


    # Sauvegarder la musique précédente AVANT de jouer la nouvelle
    if musique_en_cours:
        try:
            musique_prec = fichier_actuel
        except Exception as e:
            pass

    fichier_actuel = fichier

    try:
        musique_en_cours = pygame.mixer.Sound(fichier)
        musique_en_cours.play()
        print(f"Joue: {fichier}")
        # nom de la musique avec la note
        nom_fichier = fichier.split("/")[-1].split(".")[0]
        if len(nom_fichier) > 30:
            nom_fichier = nom_fichier[:30] + "..."
        afficher_texte_multiligne(nom_fichier, "note : " + str(trouve_note_musique(note_musique)),(38, 217, 199), (38, 217, 199))
    except Exception as e:
        print(f"Erreur lors du chargement de {fichier}: {e}")
        afficher_texte_multiligne(f"Erreur lors du chargement de {fichier}: {e}", couleur1=(255, 0, 0))

def trouve_note_musique(nombre):
    """Trouve la note d'une musique basée sur le nombre"""
    # Mapping des plages vers les notes 0-9
    if nombre == 0:
        return 0
    elif 1 <= nombre <= 2:
        return 1
    elif 3 <= nombre <= 5:
        return 2
    elif 6 <= nombre <= 9:
        return 3
    elif 10 <= nombre <= 14:
        return 4
    elif 15 <= nombre <= 20:
        return 5
    elif 21 <= nombre <= 27:
        return 6
    elif 28 <= nombre <= 35:
        return 7
    elif 36 <= nombre <= 44:
        return 8
    elif 45 <= nombre <= 54:
        return 9
    else:
        return 0  # Par défaut

def verifier_fin_musique():
    """Vérifie si la musique actuelle est terminée et lance la suivante si nécessaire"""
    global musique_en_cours, en_mode_classification, en_mode_reclassification, is_paused
    
    if musique_en_cours and not en_mode_classification and not en_mode_reclassification and not is_paused:
        # Vérifier si la musique est encore en cours de lecture
        if not pygame.mixer.get_busy():
            print("Musique terminée, lancement de la suivante...")
            jouer_nouvelle_musique()

def jouer_nouvelle_musique():
    """Joue une nouvelle musique aléatoire"""
    global note_musique, texte
    note_musique = randint(0, 54)
    jouer_musique_aleatoire()

def musique_précédente():
    global musique_en_cours, texte, is_paused
    print(musique_prec)
    if musique_prec is None:
        print("Aucune musique précédente")
        afficher_texte_multiligne("Aucune musique précédente")
        return
    try:
        # Arrêter la musique en cours
        if musique_en_cours:
            musique_en_cours.stop()
        
        # Réinitialiser l'état de pause
        is_paused = False
        
        # Jouer la musique précédente
        musique_en_cours = pygame.mixer.Sound(musique_prec)
        musique_en_cours.play() 
        print(f"Joue: {musique_prec}")
        # Afficher le nom de la musique avec la note
        # Trouver la note de la musique précédente
        categorie_prec = None
        for note, fichiers_cat in MUSIQUES_CLASSEES.items():
            if musique_prec in fichiers_cat:
                categorie_prec = note
                break

        if categorie_prec:
            note_prec = categorie_vers_note(categorie_prec)
            afficher_texte_multiligne(musique_prec.split("/")[-1].split(".")[0], "note : " + str(note_prec), (38, 217, 199), (38, 217, 199))
        else:
            afficher_texte_multiligne(musique_prec.split("/")[-1].split(".")[0], couleur1=(38, 217, 199))
    except Exception as e:
        print(f"Erreur lors du chargement de {musique_prec}: {e}")
        afficher_texte_multiligne(f"Erreur lors du chargement de {musique_prec}: {e}", couleur1= (38, 217, 199))    

def changer_note():
    """Commence la reclassification de la musique actuellement jouée"""
    global en_mode_reclassification, ancienne_categorie, fichier_actuel

    if fichier_actuel:
        en_mode_reclassification = True
        # Trouver l'ancienne catégorie de cette musique
        ancienne_categorie = trouver_categorie_musique(fichier_actuel)
        ancienne_note = categorie_vers_note(ancienne_categorie)
        afficher_texte_multiligne(f"Reclassification: {fichier_actuel.split('/')[-1].split('.')[0]}", f"Note actuelle: {ancienne_note} | 0-9: noter | +/-: ajuster | ÉCHAP: annuler", (25, 100, 255), (25, 100, 255))
        print(f"Reclassification de {fichier_actuel.split('/')[-1]}")
    else:
        afficher_texte_multiligne("Aucune musique en cours", "Jouez une musique d'abord", (255, 0, 0), (255, 0, 0))

def trouver_categorie_musique(fichier):
    """Trouve la catégorie d'une musique dans MUSIQUES_ENREGISTREES"""
    for categorie, fichiers in MUSIQUES_ENREGISTREES.items():
        if fichier in fichiers:
            return categorie
    return None

def categorie_vers_note(categorie):
    """Convertit une catégorie en note (0-9)"""
    if categorie == 0:
        return 0
    elif categorie == (1, 2):
        return 1
    elif categorie == (3, 4, 5):
        return 2
    elif categorie == (6, 7, 8, 9):
        return 3
    elif categorie == (10, 11, 12, 13, 14):
        return 4
    elif categorie == (15, 16, 17, 18, 19, 20):
        return 5
    elif categorie == (21, 22, 23, 24, 25, 26, 27):
        return 6
    elif categorie == (28, 29, 30, 31, 32, 33, 34, 35):
        return 7
    elif categorie == (36, 37, 38, 39, 40, 41, 42, 43, 44):
        return 8
    elif categorie == (45, 46, 47, 48, 49, 50, 51, 52, 53, 54):
        return 9
    else:
        return 0  # Par défaut

def retirer_musique_de_categorie(fichier, categorie):
    """Retire une musique de sa catégorie actuelle"""
    global MUSIQUES_CLASSEES, MUSIQUES_ENREGISTREES
    
    if categorie and fichier in MUSIQUES_ENREGISTREES[categorie]:
        MUSIQUES_ENREGISTREES[categorie].remove(fichier)
        MUSIQUES_CLASSEES[categorie].remove(fichier)
        print(f"Musique retirée de la catégorie {categorie}")

def reclasser_musique_actuelle(note):
    """Reclasse la musique actuellement jouée avec une nouvelle note"""
    global en_mode_reclassification, ancienne_categorie, fichier_actuel

    ancienne_categorie = trouver_categorie_musique(fichier_actuel)
    if fichier_actuel and ancienne_categorie:
        
        # Calculer l'ancienne note basée sur la catégorie
        ancienne_note = categorie_vers_note(ancienne_categorie)
        
        # Gérer les touches spéciales + et -
        if note == "+":
            nouvelle_note = ancienne_note + 1 if ancienne_note != 9 else 9
        elif note == "-":
            nouvelle_note = ancienne_note - 1 if ancienne_note != 0 else 0
        else:
            nouvelle_note = note
        
        # Retirer de l'ancienne catégorie
        retirer_musique_de_categorie(fichier_actuel, ancienne_categorie)
        
        # Ajouter à la nouvelle catégorie
        ajouter_fichier_aux_categories(fichier_actuel, nouvelle_note)
        
        # Sortir du mode reclassification
        en_mode_reclassification = False
        ancienne_categorie = None
        
        afficher_texte_multiligne(f"Musique reclassée avec la note {nouvelle_note}",None,(0, 255, 0),(255, 255, 255), temporaire=True, duree=2000)
        print(f"Musique reclassée avec la note {nouvelle_note}")
    else:
        print("Erreur: impossible de reclasser cette musique")

def annuler_reclassification():
    """Annule la reclassification en cours"""
    global en_mode_reclassification, ancienne_categorie

    en_mode_reclassification = False
    ancienne_categorie = None
    afficher_texte_multiligne("Reclassification annulée", None, (255, 205, 100))
    print("Reclassification annulée")

def toggle_pause():
    """Bascule entre pause et play"""
    global is_paused, musique_en_cours, fichier_actuel
    
    is_paused = not is_paused
    
    if musique_en_cours:
        if is_paused:
            pygame.mixer.pause()
            afficher_texte_multiligne(" PAUSE", "Appuyez sur 'ESPACE' pour reprendre", (255, 205, 100), (255, 205, 100), temporaire=True, duree=2000)
            print("Musique en pause")
        else:
            pygame.mixer.unpause()
            afficher_texte_multiligne(" LECTURE", "Appuyez sur 'ESPACE' pour pause", (0, 255, 0), (0, 255, 0), temporaire=True, duree=2000)
            print("Musique reprise")
    else:
        if is_paused:
            afficher_texte_multiligne(" PAUSE", "Aucune musique en cours", (255, 205, 100), (255, 205, 100), temporaire=True, duree=2000)
        else:
            afficher_texte_multiligne(" LECTURE", "Aucune musique en cours", (0, 255, 0), (0, 255, 0), temporaire=True, duree=2000)


# Initialiser le texte d'accueil
afficher_texte_multiligne("Appuyez sur ESPACE pour jouer une musique")



# Parcourir et classer les fichiers du répertoire Musiques
nouveaux_fichiers = parcourir_repertoire_musiques()

# Si pas de nouveaux fichiers, initialiser directement
if not nouveaux_fichiers:
    jouer_musique_aleatoire()
else:
    afficher_texte_multiligne("Nouveaux fichiers trouvés!", "Appuyez sur 'C' pour classer ou 'S' pour ignorer", (25, 100, 255), (25, 100, 255))


# Boucle principale
while launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
        elif event.type == pygame.KEYDOWN:
            if en_mode_classification:
                # Mode classification - gérer les notes 0-9
                if event.key == pygame.K_0:
                    classer_fichier_actuel(0)
                elif event.key == pygame.K_1:
                    classer_fichier_actuel(1)
                elif event.key == pygame.K_2:
                    classer_fichier_actuel(2)
                elif event.key == pygame.K_3:
                    classer_fichier_actuel(3)
                elif event.key == pygame.K_4:
                    classer_fichier_actuel(4)
                elif event.key == pygame.K_5:
                    classer_fichier_actuel(5)
                elif event.key == pygame.K_6:
                    classer_fichier_actuel(6)
                elif event.key == pygame.K_7:
                    classer_fichier_actuel(7)
                elif event.key == pygame.K_8:
                    classer_fichier_actuel(8)
                elif event.key == pygame.K_9:
                    classer_fichier_actuel(9)
                elif event.key == pygame.K_ESCAPE:
                    # Passer le fichier actuel sans le classer
                    passer_fichier_suivant()
            elif en_mode_reclassification:
                # Mode reclassification - gérer les notes 0-9 et les touches +/-
                if event.key == pygame.K_0:
                    reclasser_musique_actuelle(0)
                elif event.key == pygame.K_1:
                    reclasser_musique_actuelle(1)
                elif event.key == pygame.K_2:
                    reclasser_musique_actuelle(2)
                elif event.key == pygame.K_3:
                    reclasser_musique_actuelle(3)
                elif event.key == pygame.K_4:
                    reclasser_musique_actuelle(4)
                elif event.key == pygame.K_5:
                    reclasser_musique_actuelle(5)
                elif event.key == pygame.K_6:
                    reclasser_musique_actuelle(6)
                elif event.key == pygame.K_7:
                    reclasser_musique_actuelle(7)
                elif event.key == pygame.K_8:
                    reclasser_musique_actuelle(8)
                elif event.key == pygame.K_9:
                    reclasser_musique_actuelle(9)
                elif event.key == pygame.K_ESCAPE:
                    # Annuler la reclassification
                    annuler_reclassification()
            else:
                # Mode normal
                if event.key == pygame.K_RIGHT:
                    jouer_nouvelle_musique()
                elif event.key == pygame.K_LEFT:
                    musique_précédente()
                elif event.key == pygame.K_SPACE:
                    # Toggle pause/play
                    toggle_pause()
                elif event.key == pygame.K_c and not nouveaux_fichiers:
                    # Commencer la reclassification de la musique actuelle
                    changer_note()
                elif event.key == pygame.K_c and nouveaux_fichiers:
                    # Commencer la classification
                    commencer_classification()
                elif event.key == pygame.K_s and nouveaux_fichiers:
                    # Ignorer les nouveaux fichiers
                    ignorer_nouveaux_fichiers()
                    nouveaux_fichiers = []
                    jouer_musique_aleatoire()
                elif event.key == pygame.K_ESCAPE:
                    launched = False
                elif event.key == pygame.K_DOWN:
                    reclasser_musique_actuelle('-')
                elif event.key == pygame.K_UP:
                    reclasser_musique_actuelle('+')

    # Afficher l'image de fond
    screen.blit(image, (0,0))
    
    # Vérifier si la musique est terminée
    verifier_fin_musique()
    
    temps_actuel = pygame.time.get_ticks()
    
    # Vérifier si le message temporaire a expiré
    if message_temporaire and temps_actuel > temps_message_temporaire:
        message_temporaire = None
        message_temporaire_ligne2 = None
    
    # Afficher le message permanent (nom de la musique) en premier
    if texte is not None:
        # Centrer le texte horizontalement
        x = (window_resolution[0] - texte.get_width()) // 2
        screen.blit(texte, (x, 210))
        
        # Afficher la deuxième ligne si elle existe
        if texte_ligne2 is not None:
            x2 = (window_resolution[0] - texte_ligne2.get_width()) // 2
            screen.blit(texte_ligne2, (x2, 240))  # 40 pixels plus bas
    else:
        print("Aucun texte à afficher")
    
    # Afficher le message temporaire par-dessus si il existe
    if message_temporaire:
        # Centrer le texte horizontalement
        x = (window_resolution[0] - message_temporaire.get_width()) // 2
        screen.blit(message_temporaire, (x, 270))  # Plus bas pour ne pas écraser le nom
        
        # Afficher la deuxième ligne si elle existe
        if message_temporaire_ligne2 is not None:
            x2 = (window_resolution[0] - message_temporaire_ligne2.get_width()) // 2
            screen.blit(message_temporaire_ligne2, (x2, 300))  # 30 pixels plus bas
    
    
    pygame.display.flip()

    # Maintenir la fenêtre ouverte
    pygame.time.wait(100)  # Éviter de surcharger le CPU

# Nettoyer les ressources à la fin
pygame.quit()
print("Lecteur de musique fermé.")
