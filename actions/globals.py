from typing import List


import yaml
from pathlib import Path

def getNames(input):
    base_path = Path(__file__).parent
    file_path = (base_path / "../data/nlu.yml").resolve()
    with open(file_path, "r", encoding="utf-8") as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
        length = len(doc['nlu'])
        # print(doc['nlu'])
    data = []
    if input == 'plant_names':
        plant_names = doc['nlu'][length-2]['examples']    
        plant_list = plant_names.splitlines()
        # print(plant_list)        
        for x in plant_list:
            # print(x)
            data.append(x.replace('- ', ''))
        # print(data)        
    elif input == 'plant_problems':
        plant_probems = doc['nlu'][length-1]['examples']    
        plant_list = plant_probems.splitlines()
        # print(plant_list)        
        for x in plant_list:
            # print(x)
            data.append(x.replace('- ', ''))
        # print(data)        
        
    return data


if __name__ == "__main__":
    getNames('plant_names')