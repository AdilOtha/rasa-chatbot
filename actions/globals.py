from typing import List


import yaml
from pathlib import Path

import mysql.connector

def getNames(input, value = None):
    base_path = Path(__file__).parent
    file_path = (base_path / "../data/nlu.yml").resolve()
    with open(file_path, "r", encoding="utf-8") as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
        length = len(doc['nlu'])
        # print(doc['nlu'])
    data = []
    if input == 'plant_names':
        if value == None:
            plant_names = doc['nlu'][length-2]['examples']    
            plant_list = plant_names.splitlines()
            # print(plant_list)        
            for x in plant_list:
                # print(x)
                data.append(x.replace('- ', ''))
            # print(data)
        else:
            mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="kisan")
            mycursor = mydb.cursor(buffered=True)
            if value == 'ધાન્ય':
                value = 'અનાજ'
            sql = "SELECT DISTINCT `crop` FROM `query` WHERE `category` LIKE '%{}%'".format(value)
            mycursor.execute(sql)            
            for x in mycursor:                
                # print(x[0])
                data.append(x[0])
            print(data)
    elif input == 'plant_problems':
        plant_problems = doc['nlu'][length-1]['examples']
        plant_list = plant_problems.splitlines()
        # print(plant_list)        
        for x in plant_list:
            # print(x)
            data.append(x.replace('- ', ''))
        # print(data)
    elif input == 'plant_categories':
        plant_categories = doc['nlu'][length-3]['examples']
        plant_list = plant_categories.splitlines()
        for x in plant_list:
            # print(x)
            data.append(x.replace('- ', ''))
        
    return data


if __name__ == "__main__":
    getNames('plant_names', 'ધાન્ય')