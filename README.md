# Quiz Collaboratif

Bienvenue dans notre projet de **Quiz collaboratif** développé sous **Python** avec la bibliothèque **Pygame**. Ce quiz à choix multiple se base sur des questions de culture générale et propose 4 niveaux de difficulté pour défier vos connaissances !

## Fonctionnalités

- **4 niveaux de difficulté** : 
  - Niveau 1 = Facile
  - Niveau 2 = Moyen
  - Niveau 3 = Difficile
  - Niveau 4 = Très difficile
- **Questions culture générale** : 10 questions aléatoires couvrant différentes catégories.
- **Chronomètre** : Vous avez 30 secondes pour répondre à une question.
- **Score** : Le système de scoring permet de classer les meilleures parties.
- **Stockage des données** : Les questions, réponses, options et niveaux sont stockés dans un fichier JSON.

## Comment jouer

1. Assurez-vous d'avoir Python et Pip installé sur votre machine.
2. Installez la bibliothèque Pygame avec la commande suivante :
   ```bash
   pip install pygame
   ```
3. Clonez ce dépôt sur votre machine :
   ```bash
   git clone https://github.com/CaptainTortue/projetQuizGitAndPython.git
   ```
4. Exécutez le fichier `quiz.py` pour lancer le quiz :
   ```bash
   python quiz.py
   ```

## Règles du jeu

- Sélectionnez un niveau de difficulté parmi les 4 proposés.
- Répondez aux 10 questions à choix multiple tirées aléatoirement.
- Le chronomètre se lance à chaque question, vous avez 30 secondes pour répondre à la question.
- Gagnez des points en fonction de la rapidité et de la justesse de vos réponses.
- Consultez votre score à la fin de chaque partie.

## Structure du projet

- `quiz.py` : Point d'entrée principal du jeu, avec l'affichage et l'interface sous Pygame.
- `quizz_questions.json` : Contient les questions, options, bonnes réponses et niveaux.
- `ImportDataJSON.py` : Stocke des données dans un JSON.

## Contributions

Voici la répartition des tâches au sein de l'équipe :

- **Tony Dary** : Gestionnaire de questions (gestion de la récupération des questions et gestion du fichier des questions JSON).
- **Tristan Martinez** : Interface utilisateur (design et interaction utilisateur avec Pygame, affichage du score).
- **Aymane Merbouh** : Système de scoring (calcul du score en fonction du temps et des réponses).
- **Nicolas Delevingne** : Fonctionnalités avancées (gestion du chronomètre, création de système de difficulté).

## Licence

Ce projet est sous licence des contributeurs.

---

Merci d'avoir consulté notre projet ! N'hésitez pas à proposer vos suggestions ou à contribuer via des Pull Requests.
