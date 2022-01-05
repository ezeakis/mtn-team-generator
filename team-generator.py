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

matrix = {}

def random_team():
    random.shuffle(teams)
    return teams[0]

#initial empty matrix declaration
for team in teams:
    matrix[team] = []

for patient in patients:
    print(patient, random_team())


print(matrix)