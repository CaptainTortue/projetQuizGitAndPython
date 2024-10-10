# Example file showing a basic pygame "game loop"
import pygame

import json
import random

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
# of specific dimension..e(screenWidth, screenHeight).
BLACK = (0, 0, 0)

# assigning values to X and Y variable
screen_width = 1280
screen_height = 720

listQuestions = [
    {
        "id": 1,
        "categorie": "Science",
        "question": "Quelle planète est la plus proche du Soleil ?",
        "options": [
            "a) Mars",
            "b) Vénus",
            "c) Mercure",
            "d) Jupiter"
        ],
        "reponse": "c) Mercure"
    },
    {
        "id": 2,
        "categorie": "Animaux",
        "question": "Quel est le plus grand mammifère terrestre ?",
        "options": [
            "a) Girafe",
            "b) Eléphant",
            "c) Hippopotame",
            "d) Rhinocéros"
        ],
        "reponse": "b) Eléphant"
    }
]

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

with open('quizz_questions.json', encoding='utf-8') as questions_file:
    listQuestions = json.load(questions_file)

def randomQuestion():
    idQuestion = random.randint(1, len(listQuestions)-1)
    if listQuestions[idQuestion] in listQuestions:
        return listQuestions[idQuestion]
    else:
        return "Erreur de choix de la question"

def refreshQuestion():
    question = randomQuestion()
    text = font.render(question["question"], True, green, blue)
    textRect = text.get_rect()
    textRect.center = (screen_width // 2, screenHeight // 6)
    options = []
    optionsRect = []
    for i in range(len(question["options"])):
        option = font.render(question["options"][i], True, white, green)
        optionRect = pygame.Rect((screen_width//8 if i%2 == 0 else (screen_width//6)*4), screen_height // 6 + ((i // 2)+1) * screen_height // 4, screen_width // 4, screen_height // 6)
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

question, text, textRect, options, optionsRect, response, responseRect = refreshQuestion()

def displayRect(rect, color):
    pygame.draw.rect(screen, color, rect)
    # set the correctRect bigger
    rect.inflate_ip(10, 10)
    # refresh center of the rect
    rect.center = (screen_width // 2, screen_height // 2)
    if rect.width >= screen_width and rect.height >= screen_height:
        rect.width = screen_width // 2
        rect.height = screen_height // 2
        return False
    return True


score = 0
displayCorrectAnimation = False
displayIncorrectAnimation = False

# create green rect for correct answer animation
correctRect = pygame.Rect(screen_width // 4, screen_height // 6, screen_width // 2, screen_height // 6)

# create red rect for incorrect answer animation
incorrectRect = pygame.Rect(screen_width // 4, screen_height // 6, screen_width // 2, screen_height // 6)

# create a text surface object for the question
text = font.render(listQuestions[0]["question"], True, green, blue)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()

# Durée du timer (en millisecondes) 
start_ticks = pygame.time.get_ticks()  # Temps de démarrage du jeu
timer_duration = 30 * 1000  # 30 secondes en millisecondes

while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # poll for events
    # pygame.QUIT event means the user clicked screenWidth to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check if the mouse click was within the bounds of the option
            for i in range(len(optionsRect)):
                if optionsRect[i].collidepoint(event.pos):
                    # refresh the question
                    question, text, textRect, options, optionsRect, responses, responsesRect = refreshQuestion()
                    # check if the option clicked is the correct answer
                    if listQuestions[0]["options"][i] == listQuestions[0]["reponse"]:
                        print("Correct!")
                        score += 1
                        displayCorrectAnimation = True
                    else:
                        print("Incorrect!")
                        displayIncorrectAnimation = True
                    # display the correct answer
                    #for j in range(len(responses)):
                    #    screen.blit(responses[j], responsesRect[j])

    if (displayCorrectAnimation):
        displayCorrectAnimation = displayRect(correctRect, green)
    elif (displayIncorrectAnimation):
        displayIncorrectAnimation = displayRect(incorrectRect, red)
    else:
        # copying the text surface object
        # to the display question
        screen.blit(text, textRect)

        # copying the text surface object
        # to the display options
        for i in range(len(options)):
            # add text to the screen and rect distinctly
            # display rect for each option
            pygame.draw.rect(screen, green, optionsRect[i])
            # draw text
            screen.blit(options[i], (optionsRect[i].x + optionsRect[i].w // 2 - options[i].get_rect().w // 2, optionsRect[i].y + optionsRect[i].h // 2 - options[i].get_rect().h // 2))
        # RENDER YOUR GAME HERE

    # Calculer le temps écoulé
    elapsed_time = pygame.time.get_ticks() - start_ticks

    # Calcul du temps restant
    time_left = max(0, timer_duration - elapsed_time) // 1000  # En secondes

    # Afficher le timer restant
    timer_text = font.render(f"Temps restant: {time_left}", True, BLACK)
    screen.blit(timer_text, (screen_width // 2 - 150, screen_height // 2 - 30))

    # Si le temps est écoulé
    if time_left <= 0:
        fin_text = font.render("Temps écoulé!", True, BLACK)
        screen.blit(fin_text, (screen_width // 2 - 150, screen_height // 2 + 30))

    # copying the text surface object
    # to the display question
    screen.blit(text, textRect)

    # copying the text surface object
    # to the display options
    for i in range(len(options)):
        # add text to the screen and rect distinctly
        # display rect for each option
        pygame.draw.rect(screen, green, optionsRect[i])
        # draw text
        screen.blit(options[i], (optionsRect[i].x + optionsRect[i].w // 2 - options[i].get_rect().w // 2, optionsRect[i].y + optionsRect[i].h // 2 - options[i].get_rect().h // 2))
    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()