import json
import random

with open('quizz_questions.json', encoding='utf-8') as questions_file:
    listQuestions = json.load(questions_file)

def randomQuestion():
    idQuestion = random.randint(1, len(listQuestions))
    if listQuestions[idQuestion] in listQuestions:
        return listQuestions[idQuestion]
    else:
        return "Erreur de choix de la question"

def main():
    print("Bienvenue dans le jeu de quiz!")
    question = randomQuestion()
    print(question)


if __name__ == "__main__":
    main()