import random
import statistics

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

def balance_metric(attempt):
    teams_length = [len(team) for team in attempt.values()]
    print(teams_length)
    return statistics.mean(teams_length)



number_of_attempts = 3

space_of_attempts = []

#Initialization
for i in range(number_of_attempts):
    this_attempt = {}
    for team in teams:
        this_attempt[team] = []
    space_of_attempts.append(this_attempt)

#Assignments
for i in range(number_of_attempts):
    this_attempt = space_of_attempts[i]
    for patient in patients:
        this_attempt[random_team()].append(patient)




#Print of all assignments
for attempt in space_of_attempts:
    print("Attempt")
    print(attempt)
    print(balance_metric(attempt))
    print()
