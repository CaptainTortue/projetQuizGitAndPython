# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True


# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

# assigning values to X and Y variable
X = 1280
Y = 720

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
screen = pygame.display.set_mode((X, Y))


# set the pygame window name
pygame.display.set_caption('Show Text')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

# create a text surface object for the question
text = font.render(listQuestions[0]["question"], True, green, blue)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()

# create a rectangular object for each option possible
options = []
optionsRect = []
for i in range(len(listQuestions[0]["options"])):
    option = font.render(listQuestions[0]["options"][i], True, white, green)
    #optionRect = option.get_rect()
    #print(Y // 6 + (i // 2)+1 * 50)
    #optionRect.center = ((X//4 if i%2 == 0 else (X//4)*3), Y // 6 + ((i // 2)+1) * Y // 4)
    optionRect= pygame.Rect((X//8 if i%2 == 0 else (X//6)*4), Y // 6 + ((i // 2)+1) * Y // 4, X // 4, Y // 6)
    options.append(option)
    optionsRect.append(optionRect)

# create a rectangular object for the response
responses = []
responsesRect = []
for i in range(len(listQuestions[0]["options"])):
    response = font.render(listQuestions[0]["options"][i], True, green, blue)
    # create rect object for the question, with big size
    responseRect = pygame.Rect(X // 2, Y // 6 + (i + 1) * 50, X // 4, Y // 6)
    responses.append(response)
    responsesRect.append(responseRect)

# set the center of the rectangular object.
textRect.center = (X // 2, Y // 6)

while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


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