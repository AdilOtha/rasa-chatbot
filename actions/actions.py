# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from os import stat
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
from rasa_sdk.types import DomainDict

from .globals import nodeApiUrl, getNames, getStateNames, marketPriceUrl, stateMap , commodityMap, districtMapInvert, varietiesMapInvert

import requests


class ActionPlantProtect(Action):

    def name(self) -> Text:
        return "action_plant_protection_solution"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        entities = tracker.latest_message['entities']        

        
        plant_name = ''
        plant_problem = ''
        plant_area = ''
        print(entities)
        for e in entities:
            if e['entity'] == 'plant_name':
                plant_name = e['value']
            if e['entity'] == 'plant_problem':
                plant_problem = e['value']
            if e['entity'] == 'plant_area':
                plant_area = e['value']

        message = ''
        if plant_name == '' and plant_problem == '':
            message += "કૃપયા કરી પાક અને સમસ્યા નું નામ જણાવજો"
        elif plant_name == '':
            message += "કૃપયા કરી પાક નું નામ જણાવો"
        elif plant_problem == '':
            message += "કૃપયા કરી તમારી સમસ્યા જણાવો"

        if (plant_name != '' and plant_problem != '') or plant_area != '':
            if plant_area != '':
                message = 'અનાજના નામ:' + plant_name + ', સમસ્યાનું નામ:' + \
                    plant_problem + ' ભાગ: ' + plant_area + '\n'
            else:
                message = 'અનાજના નામ:' + plant_name + ', સમસ્યાનું નામ:' + plant_problem + '\n'
            body = {
                'plant_problem': plant_problem,
                'plant_area': plant_area,
                'plant_name': plant_name
            }            
            result = requests.post(nodeApiUrl+'kisanQuery/dataFetch',data = body)            
            response  = result.json()            
            if len(response['data']) != 0:
                print(response['data'][0])
                message += response['data'][0]['response']
            else:
                query = tracker.latest_message['text']
                print(query)
                body = {
                'query': query
                }
                result = requests.post(nodeApiUrl+'fallback/addFallback',data = body)
                print(result.status_code)
                #DataInsert(query)
                message += "માફ કરજો, અત્યારે આ જાણકારી અમારી પાસે નથી"

        dispatcher.utter_message(text=message)

        return []


class ActionPleaseRephrase(Action):
    def name(self) -> Text:
        return "action_please_rephrase"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.latest_message)
        query = tracker.latest_message['text']
        print(query)
        body = {
            'query': query
        }
        result = requests.post(nodeApiUrl+'fallback/addFallback',data = body)
        print(result.status_code)
        # DataInsert(query)

        message = "માફ કરશો, હું તે વિનંતીને સંભાળી શકતો નથી."
        dispatcher.utter_message(text=message)

        return []


class ActionPlantPrice(Action):

    def name(self) -> Text:
        return "action_plant_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        
        entities = tracker.latest_message['entities']        

        plant_name = ''
        print(entities)
        for e in entities:
            if e['entity'] == 'plant_name':
                plant_name = e['value']

        message = ''
        if plant_name == '':
            message += "કૃપયા કરી પાક નું નામ જણાવો"
        else:
            message = 'અનાજના નામ:' + plant_name + '\n'
            body = {                
                'plant_name': plant_name
            }
            result = requests.post(nodeApiUrl+'kisanQuery/getPrice',data = body)
            response  = result.json()
            if len(response['data']) != 0:
                print(response['data'][0])
                message += response['data'][0]['response']
            else:
                query = tracker.latest_message['text']
                print(query)
                body = {
                'query': query
                }
                result = requests.post(nodeApiUrl+'fallback/addFallback',data = body)
                print(result.status_code)
                #DataInsert(query)
                message += "માફ કરજો, અત્યારે આ જાણકારી અમારી પાસે નથી"

        dispatcher.utter_message(text=message)

        return []


class ActionPlantFertilizer(Action):

    def name(self) -> Text:
        return "action_plant_fertilizer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.latest_message)
        entities = tracker.latest_message['entities']

        plant_name = ''
        print(entities)
        for e in entities:
            if e['entity'] == 'plant_name':
                plant_name = e['value']

        message = ''
        if plant_name == '':
            message += "કૃપયા કરી પાક નું નામ જણાવો"
        else:
            message = 'અનાજના નામ:' + plant_name + '\n'
            body = {                
                'plant_name': plant_name
            }
            result = requests.post(nodeApiUrl+'kisanQuery/getFertilizer',data = body)
            response  = result.json()
            if len(response['data']) != 0:
                print(response['data'][0])
                message += response['data'][0]['response']
            else:
                query = tracker.latest_message['text']
                print(query)
                body = {
                'query': query
                }
                result = requests.post(nodeApiUrl+'fallback/addFallback',data = body)
                print(result.status_code)
                #DataInsert(query)
                message += "માફ કરજો, અત્યારે આ જાણકારી અમારી પાસે નથી"

        dispatcher.utter_message(text=message)

        return []

class ActionSubmit(Action):

    def name(self) -> Text:
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        print(tracker.slots)
                
        message = ''
        plant_name = tracker.get_slot("plant_name")
        plant_problem = tracker.get_slot("plant_problem")
        plant_area = tracker.get_slot("plant_area")        

        print(plant_name)
        print(plant_problem)

        if type(plant_name) is list:
            plant_name = plant_name[0]
            print(plant_name)
        if type(plant_problem) is list:
            plant_problem = plant_problem[0]
            print(plant_problem)
        if type(plant_area) is list:
            plant_area = plant_area[0]
            print(plant_area)

        if plant_area == 'સામાન્ય':
            plant_area = ''

        message = ''
        if plant_name == None and plant_problem == None:
            message += "કૃપયા કરી પાક અને સમસ્યા નું નામ જણાવજો"
        elif plant_name == None:
            message += "કૃપયા કરી પાક નું નામ જણાવો"
        elif plant_problem == None:
            message += "કૃપયા કરી તમારી સમસ્યા જણાવો"
        elif plant_name != None and plant_problem!=None:
            message = 'અનાજના નામ:' + plant_name + ', \n' + 'સમસ્યાનું નામ:'+ plant_problem + " \n"
            if plant_area != '':
                message += ' ભાગ: ' + plant_area + " \n"
            body = {
                'plant_problem': plant_problem,
                'plant_area': plant_area,
                'plant_name': plant_name
            }
            result = requests.post(nodeApiUrl+'kisanQuery/dataFetch',data = body)
            response  = result.json()
            print(response['data'])
            if len(response['data']) != 0:
                print(response['data'][0])
                message += response['data'][0]['response']
            else:
                query = plant_name + "/ " + plant_problem + "/ " + plant_area
                print(query)
                body = {
                'query': query
                }
                result = requests.post(nodeApiUrl+'fallback/addFallback',data = body)
                print(result.status_code)
                #DataInsert(query)
                message += "માફ કરજો, અત્યારે આ જાણકારી અમારી પાસે નથી"            


        dispatcher.utter_message(text=message)

        return []

class ActionFertilizerSubmit(Action):

    def name(self) -> Text:
        return "action_fertilizer_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        print(tracker.slots)
                
        message = ''
        plant_name = tracker.get_slot("plant_name")             

        print(plant_name)    

        if type(plant_name) is list:
            plant_name = plant_name[0]
            print(plant_name)        

        message = ''
        if plant_name == None:
            message += "કૃપયા કરી પાક નું નામ જણાવજો"        
        else:
            message = 'અનાજના નામ:' + plant_name + " \n"
            body = {                
                'plant_name': plant_name
            }
            result = requests.post(nodeApiUrl+'kisanQuery/getFertilizer',data = body)
            response  = result.json()
            print(response['data'])
            if len(response['data']) != 0:
                print(response['data'][0])
                message += response['data'][0]['response']
            else:
                query = tracker.latest_message['text']
                print(query)
                body = {
                'query': query + "/ ખાતર માહિતી"
                }
                result = requests.post(nodeApiUrl+'fallback/addFallback',data = body)
                print(result.status_code)
                #DataInsert(query)
                message += "માફ કરજો, અત્યારે આ જાણકારી અમારી પાસે નથી"            


        dispatcher.utter_message(text=message)

        return []        

class ActionMarketSubmit(Action):

    def name(self) -> Text:
        return "action_market_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        print(tracker.slots)        

        message = ''        
        state_name = tracker.get_slot("state_name")
        commodity_name = tracker.get_slot("commodity_name")

        print(state_name)    

        if type(state_name) is list:
            state_name = state_name[0]                        
            print(state_name)
        if type(commodity_name) is list:
            commodity_name = commodity_name[0]
            print(commodity_name)
        
        state_name_gu = state_name
        commodity_name_gu = commodity_name

        if commodity_name in commodityMap.keys() and state_name in stateMap.keys():            
            commodity_name = commodityMap[commodity_name]
            state_name = stateMap[state_name]
            
            queryParams = {'format': 'json',
            'filters[state]': state_name,
            'filters[commodity]': commodity_name
            }            

            result = requests.get(marketPriceUrl, params = queryParams)
            response  = result.json()
            print(response['records'])
            if response['count'] != 0:
                state = district = commodity = variety = ''
                print(response['records'])                
                for res in response['records']:                    

                    if res['district'] in districtMapInvert.keys():
                        district = districtMapInvert[res['district']]
                    else:
                        district = res['district']                                        
                    
                    if res['variety'] in varietiesMapInvert.keys():
                        variety = varietiesMapInvert[res['variety']]
                    else:
                        variety = res['variety']
                    
                    message += "રાજ્યનું નામ: {} \n".format(state_name_gu)
                    message +="જિલ્લાનું નામ: {} \n".format(district)                    
                    message +="ચીજવસ્તુનું નામ: {} \n".format(commodity_name_gu)
                    message +="પ્રકારનું નામ: {} \n".format(variety)
                    message +="આવવાની તારીખ: {} \n".format(res['arrival_date'])
                    message +="લઘુત્તમ ભાવ: {} \n".format(res['min_price'])
                    message +="મોડલ ભાવ: {} \n".format(res['modal_price'])
                    message +="મહત્તમ ભાવ: {} \n$".format(res['max_price'])                                       
            else:            
                message += "રાજ્યનું નામ: {}\n ચીજવસ્તુનું નામ: {}\n માફ કરજો, અત્યારે આ જાણકારી અમારી પાસે નથી".format(state_name_gu,commodity_name_gu) 
        else:
            message += "રાજ્યનું નામ: {}\n ચીજવસ્તુનું નામ: {}\n માફ કરજો, અત્યારે આ જાણકારી અમારી પાસે નથી".format(state_name_gu,commodity_name_gu)


        dispatcher.utter_message(text=message)

        return []        

class ActionSlotsReset(Action):

    def name(self) -> Text:
        return "action_slots_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:        

        return [AllSlotsReset()]

class ActionAskPlantName(Action):

    def name(self) -> Text:
        return "action_ask_plant_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        print(tracker.slots)

        plant_category = tracker.get_slot("plant_category")             

        print(plant_category)    

        if type(plant_category) is list:
            plant_category = plant_category[0]
            print(plant_category)        

        data = getNames('plant_names', plant_category)
        message={"payload":"dropDown","data":data}
        dispatcher.utter_message(text="કૃપયા કરી પાક નામ જણાવો", json_message = message)

        return []

class ActionAskPlantProblem(Action):

    def name(self) -> Text:
        return "action_ask_plant_problem"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        print(tracker.slots)        
        plant_area = tracker.get_slot('plant_area')
        if type(plant_area) is list:
            plant_area = plant_area[0]
            print(plant_area)
        if plant_area == 'રુટ':
            data = ['ફૂગ']
        else:
            data = getNames('plant_problems')
        message={"payload":"dropDown","data":data}
        dispatcher.utter_message(text="કૃપયા કરી પાક સમસ્યા જણાવો", json_message = message)

        return []

class ActionAskPlantArea(Action):

    def name(self) -> Text:
        return "action_ask_plant_area"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        print(tracker.slots)            
        data = ['રુટ', 'સામાન્ય']
        message={"payload":"dropDown","data":data}
        dispatcher.utter_message(text="કૃપયા કરી પાક ભાગ જણાવો", json_message = message)

        return []

class ActionAskPlantCategory(Action):

    def name(self) -> Text:
        return "action_ask_plant_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        print(tracker.slots)
        data = getNames('plant_categories')
        message={"payload":"dropDown","data":data}
        dispatcher.utter_message(text="કૃપયા કરી પાક વર્ગ જણાવો", json_message = message)

        return []  

class ActionAskCommodityName(Action):

    def name(self) -> Text:
        return "action_ask_commodity_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        print(tracker.slots)

        commodity_name = tracker.get_slot("commodity_name")             

        print(commodity_name)    

        if type(commodity_name) is list:
            commodity_name = commodity_name[0]
            print(commodity_name)        

        data = getNames('commodity_names')
        message={"payload":"dropDown","data":data}
        dispatcher.utter_message(text="કૃપયા કરી ચીજવસ્તુ જણાવો", json_message = message)

        return []

class ActionAskStateName(Action):

    def name(self) -> Text:
        return "action_ask_state_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        print(tracker.slots)

        state_name = tracker.get_slot("state_name")             

        print(state_name)    

        if type(state_name) is list:
            state_name = state_name[0]
            print(state_name)        

        data = getStateNames()
        message={"payload":"dropDown","data":data}
        dispatcher.utter_message(text="કૃપયા કરી રાજ્ય જણાવો", json_message = message)

        return []       