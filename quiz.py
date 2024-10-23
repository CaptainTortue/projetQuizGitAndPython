# Example file showing a basic pygame "game loop"
import pygame
import json
import random
from pathlib import Path

from ImportDataJSON import importJSON

with open('quizz_questions.json', encoding='utf-8') as questions_file:
    listQuestions = json.load(questions_file)

def randomQuestion(niveau):
    # Sélectionne tous les catégories
    categories = []
    for category in range(0, len(listQuestions) - 1 ):
        categories.append(listQuestions[category]['categorie'])

    # Filtrage pour avoir qu'une question pour 1 catégorie
    listCategories = []
    for category in categories:
        if category not in listCategories:
            listCategories.append(category)

    # lister un questionnaire avec 1 catégorie de chaque aléatoirement
    questionnaire = []

    # Initialisation de la première question par rapport au niveau dans le questionnaire
    if niveau == 1:
        idFirstQuestion = random.randint(0, 10)
        questionnaire.append(listQuestions[idFirstQuestion])
    elif niveau == 2:
        idFirstQuestion = random.randint(10, 20)
        questionnaire.append(listQuestions[idFirstQuestion])
    elif niveau == 3:
        idFirstQuestion = random.randint(20, 30)
        questionnaire.append(listQuestions[idFirstQuestion])
    elif niveau == 4:
        idFirstQuestion = random.randint(30, 40)
        questionnaire.append(listQuestions[idFirstQuestion])

    trueFalse = False

    # Boucle pour que le questionnaire soit de taille max 10
    while len(questionnaire) < 10 :
        idQuestion = random.randint(0, len(listQuestions) - 1)
        for question in questionnaire:
            # Vérification de l'existance d'une catégorie et id dans le questionnaire
            # Vérification que le niveau de la question correspond au niveau choisi
            # si True alors la question peut-être ajoutée sinon False
            if listQuestions[idQuestion]["categorie"] != question["categorie"]:
                if listQuestions[idQuestion]["id"] != question["id"]:
                    if listQuestions[idQuestion]["level"] == niveau:
                        trueFalse = True
                    else :
                        trueFalse = False
                        break
                else :
                    trueFalse = False
                    break
            else:
                trueFalse = False
                break
        if trueFalse :
            questionnaire.append(listQuestions[idQuestion])

    return questionnaire

print("Bienvenue dans le jeu de quiz!")

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True


# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)


# create the display surface object
# of specific dimension..e(screen_width, screen_height).
BLACK = (0, 0, 0)

# assigning values to X and Y variable
screen_width = 1280
screen_height = 720

# create the display surface object
# of specific dimension..e(X, Y).
screen = pygame.display.set_mode((screen_width, screen_height))

# set the pygame window name
pygame.display.set_caption('Quiz Incroyable')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)
miniFont = pygame.font.Font('freesansbold.ttf', 16)

def refreshQuestion(numQuestion, questions):
    if numQuestion >= len(questions):
        return None, None, None, None, None, True # set isEnd to False
    question = questions[numQuestion]
    text = font.render(question["question"], True, green, blue)
    textRect = text.get_rect()
    if (textRect.width > screen_width):
        text = miniFont.render(question["question"], True, green, blue)
        textRect = text.get_rect()
    textRect.center = (screen_width // 2, screen_height // 6)
    options = []
    optionsRect = []
    for i in range(len(question["options"])):
        option = font.render(question["options"][i], True, white, green)
        optionRect = pygame.Rect((screen_width//8 if i%2 == 0 else (screen_width//6)*4), screen_height // 6 + ((i // 2)+1) * screen_height // 4, screen_width // 4, screen_height // 6)
        # if option text rect is bigger than the option rect, set text in txo ligne
        if option.get_rect().width > optionRect.width:
            option = miniFont.render(question["options"][i], True, white, green)
        options.append(option)
        optionsRect.append(optionRect)
    return question, text, textRect, options, optionsRect, False

def displayRect(rect, color, question, text, textRect, options, optionsRect, numQuestion, isEnd, questions):
    pygame.draw.rect(screen, color, rect)
    # set the correctRect bigger
    rect.inflate_ip(40, 40)
    # refresh center of the rect
    rect.center = (screen_width // 2, screen_height // 2)
    if rect.width >= screen_width and rect.height >= screen_height:
        # refresh the question
        question, text, textRect, options, optionsRect, isEnd = refreshQuestion(numQuestion, questions)
        rect.width = screen_width // 2
        rect.height = screen_height // 2
        rect.center = (screen_width // 2, screen_height // 2)
        return question, text, textRect, options, optionsRect, isEnd, False
    return question, text, textRect, options, optionsRect, isEnd, True

# Fonction pour afficher l'écran de jeu
def displayGameScreen(screen, question, text, textRect, options, optionsRect, score, time_left):
    screen.fill("purple")
    # Afficher le score et le temps restant
    Score_text = font.render(f"Score : {score}", True, BLACK)
    timer_text = font.render(f"Temps restant: {time_left}", True, BLACK)
    screen.blit(Score_text, (screen_width/1.2, screen_height/50))
    screen.blit(timer_text, (screen_width/50, screen_height/50))
    # Afficher la question et les options
    if textRect and text:
        screen.blit(text, textRect)
    if optionsRect and options:
        for i in range(len(options)):
            pygame.draw.rect(screen, green, optionsRect[i])
            screen.blit(options[i], (optionsRect[i].x + optionsRect[i].w // 2 - options[i].get_rect().w // 2,
                                     optionsRect[i].y + optionsRect[i].h // 2 - options[i].get_rect().h // 2))

# Fonction pour afficher l'écran de fin
def displayEndScreen(screen, score,pseudo,total_time_left,one_execution):
    screen.fill(BLACK)
    end_text = font.render(f"Partie finie! Score: {score}.", True, white)
    screen.blit(end_text, (screen_width // 2 - end_text.get_rect().width // 2,
                           screen_height // 2 - end_text.get_rect().height // 2))
    if (one_execution==0) :
      importJSON(["name","score","Time"],[pseudo,score,total_time_left])
      one_execution+=1
      return one_execution

# Gestion des évènements
def handleEvents(running, isEnd, options, question, score, combo, numberQuestion, time_left, displayCorrectAnimation, displayIncorrectAnimation, start_ticks, difficulty, pseudo, questions, one_execution, textRect, optionsRect, text):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (isEnd):
                pseudo, difficulty, running = menu()
                numberQuestion, score, isEnd, questions, question, text, textRect, options, optionsRect, one_execution, displayCorrectAnimation, displayIncorrectAnimation = refreshGame(difficulty)
                start_ticks = pygame.time.get_ticks() + 1000  # Temps de démarrage du jeu
            # check if the mouse click was within the bounds of the option
            elif (optionsRect and options):
                for i in range(len(optionsRect)):
                    if optionsRect[i].collidepoint(event.pos):
                        numberQuestion += 1
                        # check if the option clicked is the correct answer
                        if question["options"][i] == question["reponse"]:
                            print("Correct!")
                            temp_score = 10
                            if (time_left > 28 ) :
                                temp_score *= 2
                            temp_score += time_left
                            temp_score += combo * 2
                            score += temp_score * difficulty

                            displayCorrectAnimation = True
                            combo+=1
                            start_ticks = pygame.time.get_ticks() + 1000  # Temps de démarrage du jeu

                        else:
                            print("Incorrect!")
                            combo=0
                            displayIncorrectAnimation = True
                            start_ticks = pygame.time.get_ticks() + 1000  # Temps de démarrage du jeu
    return running, isEnd, score, combo, numberQuestion, displayCorrectAnimation, displayIncorrectAnimation, start_ticks, pseudo, questions, one_execution, displayCorrectAnimation, displayIncorrectAnimation, textRect, optionsRect, options, text, question
    
# Fonction pour afficher le menu d'accueil
def displayMenu(screen, pseudo_input, selected_dificulty, start_button, Difficulty_button , leaderboard_button):
    screen.fill("lightblue")

    # Affichage du titre
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Bienvenue dans le Quiz", True, (0, 0, 0))
    screen.blit(title_text, (screen_width // 2 - title_text.get_rect().width // 2, screen_height // 6))

    # Affichage de la zone de texte pour le pseudo
    input_font = pygame.font.Font(None, 32)
    input_rect = pygame.Rect(screen_width // 4, screen_height // 3, screen_width // 2, 50)
    pygame.draw.rect(screen, (255, 255, 255), input_rect)

    # Limiter la longueur du texte à 20 caractères
    if len(pseudo_input) > 20:
        pseudo_input = pseudo_input[:20]

    # Calculer la position centrée du texte dans la zone de saisie
    pseudo_text = input_font.render(pseudo_input, True, (0, 0, 0))
    pseudo_text_rect = pseudo_text.get_rect(center=input_rect.center)
    screen.blit(pseudo_text, pseudo_text_rect)

    # Affichage du bouton Start
    button_font = pygame.font.Font(None, 48)
    pygame.draw.rect(screen, (0, 255, 0), start_button)
    start_text = button_font.render("Start", True, (0, 0, 0))
    screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_rect().width) // 2, start_button.y + 10))

    # Affichage du bouton Difficulté
    pygame.draw.rect(screen, (255, 165, 0), Difficulty_button)
    Difficulty_text = button_font.render("Difficulté", True, (0, 0, 0))
    screen.blit(Difficulty_text, (Difficulty_button.x + (Difficulty_button.width - Difficulty_text.get_rect().width) // 2, Difficulty_button.y + 10))

    # Afficher la difficulté sélectionnée
    input_font = pygame.font.Font(None, 32)
    selected_cat_text = input_font.render(f"Difficulté: {selected_dificulty}", True, (0, 0, 0))
    screen.blit(selected_cat_text, (screen_width // 2 - selected_cat_text.get_rect().width // 2, screen_height // 2 + 150))

    # Afficher le bouton Leaderboard
    pygame.draw.rect(screen, (0, 255, 0), leaderboard_button)
    leaderboard_text = font.render("Leaderboard", True, (0, 0, 0))
    screen.blit(leaderboard_text, (leaderboard_button.x + (leaderboard_button.width - leaderboard_text.get_width()) // 2,leaderboard_button.y + (leaderboard_button.height - leaderboard_text.get_height()) // 2))

    
    pygame.display.flip()
    
# Fonction pour afficher le leaderboard
def displayLeaderboard(screen,Jsondonnees):
    screen.fill((0, 0, 0))

    scores = []
    
    for objet in Jsondonnees:
        name = objet.get('name', '')        
        score = int(objet['score'])          
        timer = float(objet.get('Time', 0))   
 
        scores.append((name, score, timer))
        
    leaderboard_title = font.render("Leaderboard", True, (255, 255, 255))
    screen.blit(leaderboard_title, (screen_width // 2 - leaderboard_title.get_width() // 2, 50))
    
    scores = sorted(scores, key=lambda x: (-x[1], x[2]))
    
    # Afficher la liste des scores
    for i, (name, score, timer) in enumerate(scores):
        score_text = font.render(f"{i + 1}. {name}: {score} en {timer} sec", True, (255, 255, 255))
        screen.blit(score_text, (screen_width // 3, 150 + i * 50))

    # Afficher un bouton pour revenir au menu
    return_button = pygame.Rect(screen_width // 3, screen_height - 100, screen_width // 3, 50)
    pygame.draw.rect(screen, (0, 255, 0), return_button)
    return_text = font.render("Retour", True, (0, 0, 0))
    screen.blit(return_text, (return_button.x + (return_button.width - return_text.get_width()) // 2,
                             return_button.y + (return_button.height - return_text.get_height()) // 2))

    pygame.display.update()

    # Attendre que l'utilisateur clique sur "Retour"
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if return_button.collidepoint(mouse_pos):
                    waiting = False  # Revenir au menu
        
# Boucle principale pour le menu
def menu():
    pygame.init()
    clock = pygame.time.Clock()

    if (Path("finalscore_data.txt").is_file()):
        # Ouvrir et lire le fichier JSON
        with open('finalscore_data.json', 'r') as fichier:
            Jsondonnees = json.load(fichier)
    else :
        Jsondonnees = []
    
    pseudo_input = ""
    selected_dificulty = "Facile"
    selected_dificulty_number = 1
    running = True
    in_menu = True

    # Définir les boutons localement dans le menu
    start_button = pygame.Rect(screen_width // 3, screen_height // 2, screen_width // 3, 50)
    Difficulty_button = pygame.Rect(screen_width // 3, screen_height // 2 + 80, screen_width // 3, 50)
    leaderboard_button = pygame.Rect(screen_width // 3, screen_height // 2 + 180, screen_width // 3, 50)

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pseudo_input = pseudo_input[:-1]
                elif len(pseudo_input) < 20:
                    pseudo_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Si on clique sur le bouton Start
                if start_button.collidepoint(mouse_pos):
                    in_menu = False  # Sortir du menu et lancer le jeu

                # Si on clique sur le bouton Difficulté
                if Difficulty_button.collidepoint(mouse_pos):
                    # Changer la Difficulté
                    if selected_dificulty == "Facile":
                        selected_dificulty = "Moyen"
                        selected_dificulty_number = 2
                    elif selected_dificulty == "Moyen":
                        selected_dificulty = "Difficile"
                        selected_dificulty_number = 3
                    elif selected_dificulty == "Difficile":
                        selected_dificulty = "Très difficile"
                        selected_dificulty_number = 4
                    else:
                        selected_dificulty = "Facile"
                        selected_dificulty_number = 1
                        
                        
                # Si on clique sur le bouton Leaderboard
                if leaderboard_button.collidepoint(mouse_pos):
                    displayLeaderboard(screen,Jsondonnees)  # Afficher le leaderboard

                
                

        # Afficher le menu
        displayMenu(screen, pseudo_input, selected_dificulty, start_button, Difficulty_button, leaderboard_button)

        clock.tick(60)

    return pseudo_input, selected_dificulty_number, running

# refresh all variables for a new game
def refreshGame(difficulty):
    numberQuestion = 0
    score = 0
    displayCorrectAnimation = False
    displayIncorrectAnimation = False
    one_execution = 0
    questions = randomQuestion(difficulty)
    question, text, textRect, options, optionsRect, isEnd = refreshQuestion(numberQuestion, questions)
    return numberQuestion, score, isEnd, questions, question, text, textRect, options, optionsRect, one_execution, displayCorrectAnimation, displayIncorrectAnimation


# Boucle principale
def main():
    pygame.init()
    clock = pygame.time.Clock()
        
    # Exécuter le menu
    pseudo, difficulty, running = menu()
    
    if not running:
        pygame.quit()
        return

    # Variables globales
    one_execution = 0
    running = True
    numberQuestion = 0
    score = 0
    questions = randomQuestion(difficulty)
    

    # create green rect for correct answer animation
    correctRect = pygame.Rect(screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 6)
    correctRect.center = (screen_width // 2, screen_height // 2)

    # create red rect for incorrect answer animation
    incorrectRect = pygame.Rect(screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 6)
    incorrectRect.center = (screen_width // 2, screen_height // 2)

    # Durée du timer (en millisecondes)
    start_ticks = pygame.time.get_ticks()  # Temps de démarrage du jeu
    timer_duration = 30 * 1000  # 30 secondes en millisecondes
    combo = 0
    #total time needed calculation
    total_ticks = pygame.time.get_ticks()


    displayCorrectAnimation = False
    displayIncorrectAnimation = False

    # Charger la première question
    question, text, textRect, options, optionsRect, isEnd = refreshQuestion(numberQuestion, questions)

    while running:
        elapsed_time = pygame.time.get_ticks() - start_ticks
        time_left = max(0, timer_duration - elapsed_time) // 1000

        #calcul de total time for score/json
        elapsed_time_total = pygame.time.get_ticks() - total_ticks
        total_time_left = float(max(0, elapsed_time_total) / 1000)


        running, isEnd, score, combo, numberQuestion, displayCorrectAnimation, displayIncorrectAnimation, start_ticks, pseudo, questions, one_execution, displayCorrectAnimation, displayIncorrectAnimation, textRect, optionsRect, options, text, question = handleEvents(
            running, isEnd, options, question, score, combo, numberQuestion, time_left, displayCorrectAnimation, displayIncorrectAnimation, start_ticks ,difficulty, pseudo, questions, one_execution, textRect, optionsRect, text
        )


        # Affichage en fonction de l'état du jeu
        if isEnd:
            one_execution=displayEndScreen(screen, score,pseudo,total_time_left,one_execution)
        else:
            displayGameScreen(screen, question, text, textRect, options, optionsRect, score, time_left)

        if (displayCorrectAnimation):
            question, text, textRect, options, optionsRect, isEnd, displayCorrectAnimation = displayRect(correctRect, green, question, text, textRect, options, optionsRect, numberQuestion, isEnd, questions)
        elif (displayIncorrectAnimation):
            question, text, textRect, options, optionsRect, isEnd, displayIncorrectAnimation = displayRect(incorrectRect, red, question, text, textRect, options, optionsRect, numberQuestion, isEnd, questions)

        # Flip l'affichage pour rafraîchir l'écran
        pygame.display.flip()
        clock.tick(60)  # Limiter à 60 FPS

    pygame.quit()

# Exécution du jeu
if __name__ == "__main__":
    main()