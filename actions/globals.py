from typing import List


import yaml

def getNames(input):
    with open("C:\ME\Rasa\TestBot\data\\nlu.yml", "r", encoding="utf-8") as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
        length = len(doc['nlu'])
        # print(doc['nlu'])
    btnData = []
    if input == 'plant_names':
        plant_names = doc['nlu'][length-2]['examples']    
        plant_list = plant_names.splitlines()
        # print(plant_list)
        data = []
        for x in plant_list:
            print(x)
            data.append(x.replace('- ', ''))
        # print(data)
        for x in data:
            btnData.append(x)
        # print(btnData)
    elif input == 'plant_problems':
        plant_probems = doc['nlu'][length-1]['examples']    
        plant_list = plant_probems.splitlines()
        # print(plant_list)
        data = []
        for x in plant_list:
            print(x)
            data.append(x.replace('- ', ''))
        # print(data)    
        for x in data:
            btnData.append(x)
        # print(btnData)
        
    return btnData


if __name__ == "__main__":
    getNames('plant_names')