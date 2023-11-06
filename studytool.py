import json
import random
import os
import sys

colors = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m"
}

answered = []

# take in an input file path and return the data in the file. 
# the input file is a json
def getData(filePath):
    with open(filePath) as f:
        data = json.load(f)
    return data


# universal print function for Word to Definition and Definition to Word questions
def printQuestion(answers, answer, type):
    if type:
        print(answer["word"])
    else:
        print(answer["definition"])

    # randomly number the answers ensuring None of the above is always last
    numberedAnswers = {}
    i = 1
    while len(answers) != 0:
        choice = random.choice(list(answers.keys()))
        if choice != "None of the above":
            numberedAnswers[i] = answers[choice]
            print(str(i) + ". " + choice)
            del answers[choice]
            i += 1
        elif len(answers) == 1:
            numberedAnswers[i] = answers[choice]
            print(str(i) + ". " + choice)
            del answers[choice]
                
    # take in user input and check if it is correct. If its correct the question is added to the answered list
    userAnswer = input("Enter the number of your answer: ")
    if numberedAnswers[int(userAnswer)]:
        print(colors['green'] + "\nCorrect!" + colors['reset'] + " The answer is: " + (answer["definition"] if type else answer["word"]))
        if type:
            answered.append(answer["word"])
        else:
            answered.append(answer["definition"])
    else:
        print(colors['red'] + "\nIncorrect!" + colors['reset'] + "The answer is: " + (answer["definition"] if type else answer["word"]))


# Not implemented yet
def multipleChoiceQuestion(data, answer):
    NotAChance = random.randint(0, 2)
    return



# Take in json data and the answer to the question
# formatted as a word question with options being definitions
def wordDefQuestion(data, answer):
    
    # randomly decide if None of the above will be the answer
    NotAChance = random.randint(0, 4)
    if NotAChance != 1:
        NotAChance = 0
    used = [answer["word"], "None of the above"]
    answers = {}
    
    # get 3 random definitions (4 if the answer is None of the above) and add them to the answers dict
    while len(answers) != 3 + NotAChance:
        choice = random.choice(list(data.keys()))
        if choice not in used and type(data[choice]) == str:
            answers[data[choice]] = False
            used.append(choice)
        else:
            choice = random.choice(list(data.keys()))
            continue
    
    if NotAChance == 1:
        answers["None of the above"] = True
    else:
        answers[answer["definition"]] = True
        answers["None of the above"] = False
    
    print(colors["blue"] + "Which definition matches the following word: " + colors["reset"], end="")
    printQuestion(answers, answer, True)


# Take in json data and the answer to the question
# formatted as a definition question with options being words
def defWordQuestion(data, answer):
    NotAChance = random.randint(0, 4)
    if NotAChance != 1:
        NotAChance = 0
    used = [answer["word"], "None of the above"]
    answers = {}
    # get 3 random words (4 if the answer is None of the above) and add them to the answers dict
    while len(answers) != 3 + NotAChance:
        choice = random.choice(list(data.keys()))
        if choice not in used and type(data[choice]) == str:
            answers[choice] = False
            used.append(choice)
        else:
            choice = random.choice(list(data.keys()))
            continue
    
    if NotAChance == 1:
        answers["None of the above"] = True
    else:
        answers[answer["word"]] = True
        answers["None of the above"] = False
    
    print(colors["blue"] + "Which word matches the following definition: " + colors["reset"], end="")
    printQuestion(answers, answer, False)
    
# Sets up the question by randomly choosing the question type
def createQuestion(data):
    
    # choose what the answer will be
    answer = random.choice(list(data.keys())) 
    while answer == "None of the above":
        answer = random.choice(list(data.keys()))

    answer = {"word": answer, "definition": data[answer]}
    
    # checks to make sure data is in the correct form, then calls a random question type. (or one type has been answered, call the other)
    if type(answer["definition"]) == str:
        wDorDw = random.randint(0, 1)
        if (wDorDw == 0 and answer["word"] not in answered):
            wordDefQuestion(data, answer)
        elif (wDorDw == 1 and answer["definition"] not in answered) or (answer["word"] in answered and answer["definition"] not in answered):
            defWordQuestion(data, answer)
        else:
            return
    elif type(answer["definition"]) == dict:
        multipleChoiceQuestion(data, answer)
    else:  
        print(type(answer["definition"]))
        exit("Error: Invalid data type")

# get list of json files in current directory
currDir = sys.path[0]
json_files = [pos_json for pos_json in os.listdir(currDir) if pos_json.endswith('.json')]

print("Select a file to study: ")
for i in range(len(json_files)):
    print(str(i + 1) + ". " + json_files[i])

userInput = input("Enter the number of your selection: ")
while int(userInput) < 1 or int(userInput) > len(json_files):
    userInput = input("Enter the number of your selection: ")

filePath = currDir + "/" + json_files[int(userInput) - 1]
fileData = getData(filePath)

print()
while True:
    if len(fileData)*2 != len(answered):
        createQuestion(fileData)
        print()
    else:
        userInput = input("Enter the number of your selection: ")
        while int(userInput) < 1 or int(userInput) > len(json_files):
            userInput = input("Enter the number of your selection: ")

        filePath = currDir + "/" + json_files[int(userInput) - 1]
        fileData = getData(filePath)
    
    