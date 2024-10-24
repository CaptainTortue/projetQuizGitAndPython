# Example file showing a basic pygame "game loop"
import pygame
import json
import random
from pathlib import Path

from ImportDataJSON import importJSON

with open('quizz_questions.json', encoding='utf-8') as questions_file:
    listQuestions = json.load(questions_file)

pygame.mixer.init()

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True


# Define the RGB value for white, green, blue, and red
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
gold = (255, 215, 0)
greendarker = (58,178,26)

# Create the display surface object of specific dimension (screen_width, screen_height)
BLACK = (0, 0, 0)

# Assign values to screen width and height variables
screen_width = 1280
screen_height = 720

# Create the display surface object of specific dimensions
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the pygame window name
pygame.display.set_caption('Incredible Quiz')

# Create a font object
# 1st parameter is the font file present in pygame
# 2nd parameter is the font size
font = pygame.font.Font('freesansbold.ttf', 32)
miniFont = pygame.font.Font('freesansbold.ttf', 16)


# Fonction to show the timer bar and the timer
def show_timer(screen, font, start_ticks, timer_duration, screen_width, screen_height):
    elapsed_time = pygame.time.get_ticks() - start_ticks

    # Calcul of the time left
    time_left = max(0, timer_duration - elapsed_time) // 1000  # En secondes

    #show the time text
    timer_text = font.render(f"Temps restant: {time_left}", True, BLACK)
    screen.blit(timer_text, (screen_width // 50, screen_height // 50))  # Position (x, y)

    # size and position of the bar
    bar_width = screen_width 
    bar_height = screen_height *5/100
    bar_x = screen_width - screen_width
    bar_y = screen_height - screen_height *5/100

    proportion_time_left = (timer_duration - elapsed_time) / timer_duration

    current_bar_width = max(0, proportion_time_left * bar_width)

    pygame.draw.rect(screen, "lightblue" , (bar_x, bar_y, bar_width, bar_height))

    pygame.draw.rect(screen, greendarker, (bar_x, bar_y, current_bar_width, bar_height))

    return time_left

def randomQuestion(niveau):
    # Selects all categories
    categories = []
    for category in range(0, len(listQuestions) - 1):
        categories.append(listQuestions[category]['categorie'])

    # Filtering to have only one question for each category
    listCategories = []
    for category in categories:
        if category not in listCategories:
            listCategories.append(category)

    # List a quiz with one question from each category randomly
    questionnaire = []

    # Initialize the first question according to the level in the quiz
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

    # Loop to ensure the quiz has a max size of 10 questions
    while len(questionnaire) < 10:
        idQuestion = random.randint(0, len(listQuestions) - 1)
        for question in questionnaire:
            # Check for category and ID existence in the quiz
            # Ensure the question level matches the selected level
            # If true, the question can be added, otherwise false
            if listQuestions[idQuestion]["categorie"] != question["categorie"]:
                if listQuestions[idQuestion]["id"] != question["id"]:
                    if listQuestions[idQuestion]["level"] == niveau:
                        trueFalse = True
                    else:
                        trueFalse = False
                        break
                else:
                    trueFalse = False
                    break
            else:
                trueFalse = False
                break
        if trueFalse:
            questionnaire.append(listQuestions[idQuestion])

    return questionnaire

print("Bienvenue dans le jeu de quiz!")


def refreshQuestion(numQuestion, questions):
    if numQuestion >= len(questions):
        return None, None, None, None, None, True  # set isEnd to True
    question = questions[numQuestion]
    text = font.render(question["question"], True, BLACK)
    textRect = text.get_rect()
    if textRect.width > screen_width:
        text = miniFont.render(question["question"], True, green, blue)
        textRect = text.get_rect()
    textRect.center = (screen_width // 2, screen_height // 6)
    options = []
    optionsRect = []
    for i in range(len(question["options"])):
        option = font.render(question["options"][i], True, white, green)
        optionRect = pygame.Rect(
            (screen_width // 8 if i % 2 == 0 else (screen_width // 6) * 4),
            screen_height // 6 + ((i // 2) + 1) * screen_height // 4,
            screen_width // 4, screen_height // 6)
        # If option text rect is bigger than the option rect, set text in two lines
        if option.get_rect().width > optionRect.width:
            option = miniFont.render(question["options"][i], True, white, green)
        options.append(option)
        optionsRect.append(optionRect)
    return question, text, textRect, options, optionsRect, False

def displayRect(rect, color, question, text, textRect, options, optionsRect, numQuestion, isEnd, questions):
    pygame.draw.rect(screen, color, rect,border_radius=20)
    # Make the correctRect larger
    rect.inflate_ip(40, 40)
    # Refresh the center of the rect
    rect.center = (screen_width // 2, screen_height // 2)
    if rect.width >= screen_width and rect.height >= screen_height:
        # Refresh the question
        question, text, textRect, options, optionsRect, isEnd = refreshQuestion(numQuestion, questions)
        rect.width = screen_width // 2
        rect.height = screen_height // 2
        rect.center = (screen_width // 2, screen_height // 2)
        return question, text, textRect, options, optionsRect, isEnd, False
    return question, text, textRect, options, optionsRect, isEnd, True

# Function to display the game screen
def displayGameScreen(screen, question, text, textRect, options, optionsRect, score, time_left,start_ticks,timer_duration):
    screen.fill("lightblue")

    # Display score and remaining time
    Score_text = font.render(f"Score : {score}", True, BLACK)
    show_timer(screen, font, start_ticks, timer_duration, screen_width, screen_height)
    timer_text = font.render(f"Temps restant: {time_left}", True, BLACK)
    screen.blit(Score_text, (screen_width / 1.2, screen_height / 50))
    screen.blit(timer_text, (screen_width / 50, screen_height / 50))
    # Display the question and options
    if textRect and text:
        screen.blit(text, textRect)
    if optionsRect and options:
        for i in range(len(options)):
            pygame.draw.rect(screen, green, optionsRect[i], border_radius=20)

            screen.blit(options[i], (optionsRect[i].x + optionsRect[i].w // 2 - options[i].get_rect().w // 2,
                                     optionsRect[i].y + optionsRect[i].h // 2 - options[i].get_rect().h // 2))

# Function to display the end screen
def displayEndScreen(screen, score, pseudo, total_time_left, one_execution):
    screen.fill(BLACK)
    end_text = font.render(f"Partie finie! Score: {score}.", True, white)
    screen.blit(end_text, (screen_width // 2 - end_text.get_rect().width // 2,
                           screen_height // 2 - end_text.get_rect().height // 2))
    
    if one_execution == 0:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("ENDINGPRO.mp3")
        # Définir le volume de la musique (0.0 à 1.0)
        pygame.mixer.music.set_volume(0.9)

        # Jouer la musique en boucle (-1 signifie répétition infinie)
        pygame.mixer.music.play(-1)
        importJSON(["name", "score", "Time"], [pseudo, score, total_time_left])
        one_execution += 1
        return one_execution

# Event handling
def handleEvents(running, isEnd, options, question, score, combo, numberQuestion, time_left, displayCorrectAnimation, displayIncorrectAnimation, start_ticks, difficulty, pseudo, questions, one_execution, textRect, optionsRect, text):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if isEnd:
                pseudo, difficulty, running = menu()
                numberQuestion, score, isEnd, questions, question, text, textRect, options, optionsRect, one_execution, displayCorrectAnimation, displayIncorrectAnimation = refreshGame(difficulty)
                start_ticks = pygame.time.get_ticks() + 1000  # Game start time
            # Check if the mouse click was within the bounds of the option
            elif optionsRect and options:
                for i in range(len(optionsRect)):
                    if optionsRect[i].collidepoint(event.pos):
                        numberQuestion += 1
                        # Check if the clicked option is the correct answer
                        if question["options"][i] == question["reponse"]:
                            print("Correct!")
                            temp_score = 10
                            if time_left > 28:
                                temp_score *= 2
                            temp_score += time_left
                            temp_score += combo * 2
                            score += temp_score * difficulty

                            displayCorrectAnimation = True
                            combo += 1
                            start_ticks = pygame.time.get_ticks() + 1000  # Game start time

                        else:
                            print("Incorrect!")
                            combo = 0
                            displayIncorrectAnimation = True
                            start_ticks = pygame.time.get_ticks() + 1000  # Game start time
    return running, isEnd, score, combo, numberQuestion, displayCorrectAnimation, displayIncorrectAnimation, start_ticks, pseudo, questions, one_execution, displayCorrectAnimation, displayIncorrectAnimation, textRect, optionsRect, options, text, question, difficulty

# Function to display the main menu
def displayMenu(screen, pseudo_input, selected_dificulty, start_button, Difficulty_button, leaderboard_button):
    screen.fill("lightblue")

    # Display the title
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Bienvenue dans le Quiz", True, (0, 0, 0))
    screen.blit(title_text, (screen_width // 2 - title_text.get_rect().width // 2, screen_height // 6))

    # Display the text input field for the pseudo
    input_font = pygame.font.Font(None, 32)
    input_rect = pygame.Rect(screen_width // 4, screen_height // 3, screen_width // 2, 50)
    pygame.draw.rect(screen,(255, 255, 255), input_rect, border_radius=20)

    # Limit text length to 20 characters
    if len(pseudo_input) > 20:
        pseudo_input = pseudo_input[:20]

    # Center the text inside the input field
    pseudo_text = input_font.render(pseudo_input, True, (0, 0, 0))
    pseudo_text_rect = pseudo_text.get_rect(center=input_rect.center)
    screen.blit(pseudo_text, pseudo_text_rect)

    # Display the Start button
    button_font = pygame.font.Font(None, 48)
    pygame.draw.rect(screen, (0, 255, 0), start_button ,border_radius=20)

    start_text = button_font.render("Start", True, (0, 0, 0))
    screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_rect().width) // 2, start_button.y + 10))

    # Display the Difficulty button
    pygame.draw.rect(screen, (255, 165, 0), Difficulty_button ,border_radius=20)
    Difficulty_text = button_font.render("Difficulty", True, (0, 0, 0))
    screen.blit(Difficulty_text, (Difficulty_button.x + (Difficulty_button.width - Difficulty_text.get_rect().width) // 2, Difficulty_button.y + 10))

    # Display the selected difficulty
    input_font = pygame.font.Font(None, 32)
    selected_cat_text = input_font.render(f"Difficulté: {selected_dificulty}", True, (0, 0, 0))
    screen.blit(selected_cat_text, (screen_width // 2 - selected_cat_text.get_rect().width // 2, screen_height // 2 + 150))

    # Display the Leaderboard button
    pygame.draw.rect(screen, (0, 255, 0), leaderboard_button,border_radius=20)
    leaderboard_text = font.render("Leaderboard", True, (0, 0, 0))
    screen.blit(leaderboard_text, (leaderboard_button.x + (leaderboard_button.width - leaderboard_text.get_width()) // 2,
                                   leaderboard_button.y + (leaderboard_button.height - leaderboard_text.get_height()) // 2))

    pygame.display.flip()

# Function to display the leaderboard
def displayLeaderboard(screen, Jsondonnees):
    screen.fill("lightblue")

    scores = []

    # Parse the JSON data for names, scores, and time
    for objet in Jsondonnees:
        name = objet.get('name', '')
        score = int(objet['score'])
        timer = float(objet.get('Time', 0))

        scores.append((name, score, timer))
        # Draw a rectangle as a background for the leaderboard
        leaderboard_bg_rect = pygame.Rect(screen_width // 4, 100, screen_width // 2, screen_height - 220)
        pygame.draw.rect(screen, (255, 255, 255), leaderboard_bg_rect,
                         border_radius=20)  # Dark gray background with rounded corners
    # Display the leaderboard title
    leaderboard_title = font.render("Leaderboard", True, (0, 0, 0))
    screen.blit(leaderboard_title, (screen_width // 2 - leaderboard_title.get_width() // 2, 50))

    # Sort the scores first by highest score and then by lowest time
    scores = sorted(scores, key=lambda x: (-x[1], x[2]))

    # Display the list of scores
    for i, (name, score, timer) in enumerate(scores):
        if i >= 8: # Display only the top 8 scores
            break
        score_text = font.render(f"{i + 1}. {name}: {score} in {timer} sec", True, (0, 0, 0))
        screen.blit(score_text, (screen_width // 3, 150 + i * 50))

    # Display a button to return to the menu
    return_button = pygame.Rect(screen_width // 3, screen_height - 100, screen_width // 3, 50)
    pygame.draw.rect(screen, (0, 255, 0), return_button,border_radius=20)
    return_text = font.render("Return", True, (0, 0, 0))
    screen.blit(return_text, (return_button.x + (return_button.width - return_text.get_width()) // 2,
                              return_button.y + (return_button.height - return_text.get_height()) // 2))

    pygame.display.update()

    # Wait for the user to click on "Return"
    waiting = True
    running = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if return_button.collidepoint(mouse_pos):
                    waiting = False  # Return to the menu
                    running = True
    return running

# Main loop for the menu
def menu():
    pygame.init()
    clock = pygame.time.Clock()

    pygame.mixer.music.load("MusicMenuProfessionel.mp3")
    # Définir le volume de la musique (0.0 à 1.0)
    pygame.mixer.music.set_volume(0.5)

    # Jouer la musique en boucle (-1 signifie répétition infinie)
    pygame.mixer.music.play(-1)

    # Check if the score file exists, load JSON data if it does
    if (Path("finalscore_data.json").is_file()):
        # Open and read the JSON file
        with open('finalscore_data.json', 'r') as fichier:
            Jsondonnees = json.load(fichier)
    else:
        Jsondonnees = []

    pseudo_input = ""
    selected_dificulty = "Facile"
    selected_dificulty_number = 1
    running = True
    in_menu = True

    # Define buttons locally within the menu
    start_button = pygame.Rect(screen_width // 3, screen_height // 2, screen_width // 3, 50)
    Difficulty_button = pygame.Rect(screen_width // 3, screen_height // 2 + 80, screen_width // 3, 50)
    leaderboard_button = pygame.Rect(screen_width // 3, screen_height // 2 + 180, screen_width // 3, 50)

    while in_menu and running:

        # Display the menu
        displayMenu(screen, pseudo_input, selected_dificulty, start_button, Difficulty_button, leaderboard_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                running = False

            # Handle text input for the pseudo field
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pseudo_input = pseudo_input[:-1]
                elif len(pseudo_input) < 20:
                    pseudo_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # If "Start" button is clicked
                if start_button.collidepoint(mouse_pos):
                    in_menu = False  # Exit the menu and start the game
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("QCMMusicProfessional.mp3")
                    # Définir le volume de la musique (0.0 à 1.0)
                    pygame.mixer.music.set_volume(0.5)

                    # Jouer la musique en boucle (-1 signifie répétition infinie)
                    pygame.mixer.music.play(-1)


                # If "Difficulty" button is clicked
                if Difficulty_button.collidepoint(mouse_pos):
                    # Cycle through difficulty levels
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

                # If "Leaderboard" button is clicked
                if leaderboard_button.collidepoint(mouse_pos):
                    running = displayLeaderboard(screen, Jsondonnees)  # Display the leaderboard

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

# Main loop
def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Run the menu
    pseudo, difficulty, running = menu()


    

    if running:
        one_execution = 0
        numberQuestion = 0
        score = 0
        questions = randomQuestion(difficulty)

        # Create a green rectangle for correct answer animation
        correctRect = pygame.Rect(screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 6)
        correctRect.center = (screen_width // 2, screen_height // 2)

        # Create a red rectangle for incorrect answer animation
        incorrectRect = pygame.Rect(screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 6)
        incorrectRect.center = (screen_width // 2, screen_height // 2)

        # Timer duration (in milliseconds)
        start_ticks = pygame.time.get_ticks()  # Record the start time of the game
        timer_duration = 30 * 1000  # 30-second timer in milliseconds
        combo = 0

        # Calculate total time needed
        total_ticks = pygame.time.get_ticks()

        displayCorrectAnimation = False
        displayIncorrectAnimation = False

        # Load the first question
        question, text, textRect, options, optionsRect, isEnd = refreshQuestion(numberQuestion, questions)

    while running:
        elapsed_time = pygame.time.get_ticks() - start_ticks  # Time elapsed since the start of the question
        time_left = max(0, timer_duration - elapsed_time) // 1000  # Remaining time for the question (in seconds)

        # Calculate the total elapsed time for the score and JSON data
        elapsed_time_total = pygame.time.get_ticks() - total_ticks
        total_time_left = float(max(0, elapsed_time_total) / 1000)

        # Handle game events (responses, transitions, etc.)
        running, isEnd, score, combo, numberQuestion, displayCorrectAnimation, displayIncorrectAnimation, start_ticks, pseudo, questions, one_execution, displayCorrectAnimation, displayIncorrectAnimation, textRect, optionsRect, options, text, question, difficulty = handleEvents(
            running, isEnd, options, question, score, combo, numberQuestion, time_left, displayCorrectAnimation, displayIncorrectAnimation, start_ticks, difficulty, pseudo, questions, one_execution, textRect, optionsRect, text
        )

        # Display elements based on the current game state
        if isEnd:
            one_execution = displayEndScreen(screen, score, pseudo, total_time_left, one_execution)
        else:
            displayGameScreen(screen, question, text, textRect, options, optionsRect, score, time_left,start_ticks,timer_duration)

        # Show correct or incorrect answer animation
        if displayCorrectAnimation:
            question, text, textRect, options, optionsRect, isEnd, displayCorrectAnimation = displayRect(correctRect, green, question, text, textRect, options, optionsRect, numberQuestion, isEnd, questions)
        elif displayIncorrectAnimation:
            question, text, textRect, options, optionsRect, isEnd, displayIncorrectAnimation = displayRect(incorrectRect, red, question, text, textRect, options, optionsRect, numberQuestion, isEnd, questions)

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
