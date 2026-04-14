import pycurl
import json
import random
from io import BytesIO
import sqlite3

db:str = 'fitness.db'

def getSuggestionData(url:str, account:int):
    #pycurl call to API Ninjas
    curl = pycurl.Curl()
    buffer = BytesIO()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, ['X-Api-Key: WH8t1WdYIZ4kRKOWN6CNknnxhGVLGP9dKueueBVN'])
    curl.setopt(curl.WRITEDATA, buffer)
    curl.perform()
    curl.close()
    
    jsonData = json.loads(buffer.getvalue().decode('utf-8'))

    if not jsonData:
        return {"Suggestion": [{'name': 'None', 'instructions': 'None', 'safety_info': 'None'}]}

    if 'error' in jsonData:
        return {"Suggestion": [{'name': 'Error', 'instructions': jsonData['error'], 'safety_info': 'NA'}]}
    
    #Parsing JSON Result
    suggestionData = [{i: obj[i] for i in ['name', 'instructions', 'safety_info'] if i in obj} for obj in jsonData]

    #Obtain Rating Weights
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql:str = "SELECT exercise_name, rating FROM exercise_ratings WHERE user_id = 1;"
    cursor.execute(sql)
    ratings = cursor.fetchall()
    connection.close()
    ratingsExercise =  {row[0]: row[1] for row in ratings}

    #Applying Rating Weights    
    weights = []
    for exercise in suggestionData:
        name = exercise.get('name')
        if name in ratingsExercise:
            #print(name + " : " + str(ratingsExercise[name]))
            weights.append(ratingsExercise[name]) 
        else:
            #print(name + " : 1")
             weights.append(1)   
    
    #Randon Select with Weights
    suggestion = random.choices(suggestionData, weights=weights, k=1)
    #print(suggestion)
    return {"Suggestion": suggestion}
