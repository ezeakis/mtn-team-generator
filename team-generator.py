import random

patients = [
    "patient1", 
    "patient2", 
    "patient3", 
    "patient4", 
    "patient5", 
    "patient6", 
    "patient7", 
    "patient8", 
]

teams = [
    "team1", 
    "team2", 
    "team3", 
    "team4", 
]

def random_team():
    random.shuffle(teams)
    return teams[0]

number_of_attempts = 3

space_of_attempts = []

#Initialization
for i in range(number_of_attempts):
    this_attempt = {}
    for team in teams:
        attempt[team] = []
    space_of_attempts.append(this_attempt)




# for patient in patients:
#     print(patient, random_team())
#     matrix[random_team()].append(patient)



print(space_of_attempts)