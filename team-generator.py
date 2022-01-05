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

emp = db.Table('emp', metadata,
              db.Column('Id', db.Integer()),
              db.Column('name', db.String(255), nullable=False),
              db.Column('salary', db.Float(), default=100.0),
              db.Column('active', db.Boolean(), default=True)
              )

metadata.create_all(engine) #Creates the table

#Inserting record one by one
query = db.insert(emp).values(Id=1, name='naveen', salary=60000.00, active=True) 
ResultProxy = connection.execute(query)

#Inserting many records at ones
query = db.insert(emp) 
values_list = [{'Id':'2', 'name':'ram', 'salary':80000, 'active':False},
               {'Id':'3', 'name':'ramesh', 'salary':70000, 'active':True}]
ResultProxy = connection.execute(query,values_list)

results = connection.execute(db.select([emp])).fetchall()
df = pd.DataFrame(results)
df.columns = results[0].keys()
print(df.head(4))