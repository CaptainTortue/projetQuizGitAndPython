# Example file showing a basic pygame "game loop"
import pygame

import json
import random

with open('quizz_questions.json', encoding='utf-8') as questions_file:
    listQuestions = json.load(questions_file)

def randomQuestion():
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

    # Initialisation de la première question dans le questionnaire
    idFirstQuestion = random.randint(0, len(listQuestions) - 1)
    questionnaire.append(listQuestions[idFirstQuestion])

    trueFalse = False

    # Boucle pour que le questionnaire soit de taille max 10
    while len(questionnaire) < 10 :
        idQuestion = random.randint(0, len(listQuestions) - 1)
        for question in questionnaire:
            # Vérification de l'existance d'une catégorie et id dans le questionnaire
            # si True alors la question peut-être ajoutée sinon False
            if listQuestions[idQuestion]["categorie"] != question["categorie"]:
                if listQuestions[idQuestion]["id"] != question["id"]:
                    trueFalse = True
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
pygame.display.set_caption('Show Text')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)
miniFont = pygame.font.Font('freesansbold.ttf', 16)

questions = randomQuestion()

for i in range(len(questions) - 1):
    print(questions[i]['id'], " ", questions[i]['categorie'] )

numberQuestion = 0

def refreshQuestion(numQuestion):
    if numQuestion >= len(questions):
        global isEnd
        isEnd = True
        return None, None, None, None, None, None, None
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
    responses = []
    responsesRect = []
    for i in range(len(question["options"])):
        response = font.render(question["options"][i], True, green, blue)
        responseRect = pygame.Rect(screen_width // 2, screen_height // 6 + (i + 1) * 50, screen_width // 4, screen_height // 6)
        responses.append(response)
        responsesRect.append(responseRect)
    return question, text, textRect, options, optionsRect, responses, responsesRect

question, text, textRect, options, optionsRect, response, responseRect = refreshQuestion(numberQuestion)

def displayRect(rect, color):
    pygame.draw.rect(screen, color, rect)
    # set the correctRect bigger
    rect.inflate_ip(40, 40)
    # refresh center of the rect
    rect.center = (screen_width // 2, screen_height // 2)
    if rect.width >= screen_width and rect.height >= screen_height:
        # refresh the question
        global question, text, textRect, options, optionsRect, responses, responsesRect
        question, text, textRect, options, optionsRect, responses, responsesRect = refreshQuestion(numberQuestion)
        rect.width = screen_width // 2
        rect.height = screen_height // 2
        rect.center = (screen_width // 2, screen_height // 2)
        return False
    return True


score = 0
displayCorrectAnimation = False
displayIncorrectAnimation = False

isEnd = False

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

while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # Calculer le temps écoulé
    elapsed_time = pygame.time.get_ticks() - start_ticks

    # Calcul du temps restant
    time_left = max(0, timer_duration - elapsed_time) // 1000  # En secondes

    # poll for events
    # pygame.QUIT event means the user clicked screen_width to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (isEnd):
                running = False
            # check if the mouse click was within the bounds of the option
            if (optionsRect and options):
              for i in range(len(optionsRect)):
                  if optionsRect[i].collidepoint(event.pos):
                      numberQuestion += 1
                      # check if the option clicked is the correct answer
                      if question["options"][i] == question["reponse"]:
                          print(question["options"][i], question["reponse"])
                          print("Correct!")
                          temp_score = 10
                          if (time_left > 28 ) : 
                              temp_score *= 2
                          temp_score += time_left
                          temp_score += combo * 2
                          score += temp_score

                          displayCorrectAnimation = True
                          combo+=1
                          start_ticks = pygame.time.get_ticks() + 1000  # Temps de démarrage du jeu

                      else:
                          print("Incorrect!")
                          combo=0
                          displayIncorrectAnimation = True
                          start_ticks = pygame.time.get_ticks() + 1000  # Temps de démarrage du jeu

                      # display the correct answer
                      #for j in range(len(responses)):
                      #    screen.blit(responses[j], responsesRect[j])


    # Afficher le timer restant
    timer_text = font.render(f"Temps restant: {time_left}", True, BLACK)
    screen.blit(timer_text, (screen_width/50,screen_height/50))

    # Si le temps est écoulé
    if time_left <= 0:
        combo=0
        displayIncorrectAnimation = True
        numberQuestion+=1
        start_ticks = pygame.time.get_ticks() + 1000  # Temps de démarrage du jeu


    #ajout du text score total  
    Score_text = font.render(f"Score : {score}",True,BLACK)
    screen.blit(Score_text, (screen_width/1.2,screen_height/50))

 
    # copying the text surface object
    # to the display question
    if (textRect and text):
        screen.blit(text, textRect)

   # RENDER YOUR GAME HERE
    if (displayCorrectAnimation):
        displayCorrectAnimation = displayRect(correctRect, green)
    elif (displayIncorrectAnimation):
        displayIncorrectAnimation = displayRect(incorrectRect, red)
    else:
        # copying the text surface object
        # to the display question
        if (textRect and text):
            screen.blit(text, textRect)

        # copying the text surface object
        # to the display options
        if (optionsRect and options):
            for i in range(len(options)):
                # add text to the screen and rect distinctly
                # display rect for each option
                pygame.draw.rect(screen, green, optionsRect[i])
                # draw text
                screen.blit(options[i], (optionsRect[i].x + optionsRect[i].w // 2 - options[i].get_rect().w // 2, optionsRect[i].y + optionsRect[i].h // 2 - options[i].get_rect().h // 2))
        # RENDER YOUR GAME HERE

    if (isEnd):
        screen.fill(BLACK)
        end_text = font.render(f"Partie fini !!! Score: {score}. ", True, white)
        screen.blit(end_text, (screen_width // 2 - end_text.get_rect().width // 2, screen_height // 2 - end_text.get_rect().height // 2))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()