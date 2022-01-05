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
    #standard deviation
    return statistics.stdev(teams_length)



number_of_attempts = 10

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

#Choose the attempts with better balance metric
balance_metrics_list = [balance_metric(attempt) for attempt in space_of_attempts]
optimum_balance_metric = min(balance_metrics_list)
reduced_attempts_list = [attempt for attempt in space_of_attempts if  balance_metric(attempt) == optimum_balance_metric]
print("Optimum Attempts")
for attempt in reduced_attempts_list:
    print(attempt)

#DB insert
import sqlalchemy as db
import pandas as pd

engine = db.create_engine('sqlite:///test.sqlite') #Create test.sqlite automatically
connection = engine.connect()
metadata = db.MetaData()


patients_table = db.Table('patients', metadata,
              db.Column('patient_name', db.String(255), nullable=False),
              db.Column('team_name', db.String(255), nullable=True),
              )
teams_table = db.Table('teams', metadata,
              db.Column('team_name', db.String(255), nullable=False),
              db.Column('balance_metric', db.Integer(), nullable=True),
              )
metadata.create_all(engine) #Creates the table

#Inserting record one by one
#query = db.insert(emp).values(Id=1, name='naveen', salary=60000.00, active=True) 
#ResultProxy = connection.execute(query)

#Inserting many records at ones
# query = db.insert(patients_table) 
# values_list = []
# for patient in patients:
#     values_list.append({'name':patient,})
# ResultProxy = connection.execute(query,values_list)

# results = connection.execute(db.select([patients_table])).fetchall()
# df = pd.DataFrame(results)
# df.columns = results[0].keys()
# print(df.head(10))

print("Displaying all patients")
patients_results = connection.execute(db.select([patients_table])).fetchall()
if int(len(patients_results)) != 0:
    patients_df = pd.DataFrame(patients_results)
    patients_df.columns = patients_results[0].keys()
    print(patients_df.head(10))
print()


print("Displaying all teams")
teams_results = connection.execute(db.select([teams_table])).fetchall()
if int(len(teams_results)) != 0:
    teams_df = pd.DataFrame(teams_results)
    teams_df.columns = teams_results[0].keys()
    print(teams_df.head(10))
print()


print("Calculating balance metrics...")
teams_results = connection.execute(db.select([teams_table.columns.team_name])).fetchall()
print(teams_results)
if int(len(teams_results)) != 0:
    for team in teams_results:
        specific_patients_results = connection.execute(db.select([patients_table]).where(patients_table.columns.team_name == team)).fetchall()
        #if int(len(specific_patients_results)) != 0:
        #    print(specific_patients_results)
        query = db.update(teams_table).values(balance_metric = int(len(specific_patients_results)))
        query = query.where(teams_table.columns.team_name == team)
        results = connection.execute(query)
    print()


print("Please choose an action")
print("1 for adding a patient")
print("2 for adding a team")
print("3 for listing patients")
print("4 for listing teams")
print("5 for assigning next non-assigned patient to a team")
action = input("Choose: ")

if action == "1":
    this_name = input("Declare patient name: ")
    query = db.insert(patients_table).values(patient_name=this_name,) 
    ResultProxy = connection.execute(query)

elif action == "2":
    this_name = input("Declare team name: ")
    query = db.insert(teams_table).values(team_name=this_name,) 
    ResultProxy = connection.execute(query)

elif action == "3":
    results = connection.execute(db.select([patients_table])).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    print(df.head(10))

elif action == "4":
    results = connection.execute(db.select([teams_table])).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    print(df.head(10))

elif action == "5":
    unassigned_patients_results = connection.execute(db.select([patients_table]).where(patients_table.columns.team_name == None)).fetchall()
    if int(len(unassigned_patients_results)) != 0:
        unassigned_patients_df = pd.DataFrame(unassigned_patients_results)
        unassigned_patients_df.columns = unassigned_patients_results[0].keys()
        print(unassigned_patients_df.head(10))
    print()

    teams_balance_metrics_list = connection.execute(db.select([teams_table.columns.balance_metric.distinct()])).fetchall()
    minimum_balance_metric = min([i[0] for i in teams_balance_metrics_list])
    print(minimum_balance_metric)

    teams_results_with_minimum_balance_metric = connection.execute(db.select([teams_table]).where(teams_table.columns.balance_metric == minimum_balance_metric)).fetchall()
    random.shuffle(teams_results_with_minimum_balance_metric)

    print(teams_results_with_minimum_balance_metric)

    chosen_team = teams_results_with_minimum_balance_metric[0][0]
    print("chosen team: ", chosen_team)

    next_unassigned_patient = unassigned_patients_results[0][0]
    print("next_unassigned_patient: ", next_unassigned_patient)

    query = db.update(patients_table).values(team_name = chosen_team)
    query = query.where(patients_table.columns.patient_name == next_unassigned_patient)
    results = connection.execute(query)