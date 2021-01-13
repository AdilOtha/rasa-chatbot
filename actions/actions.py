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

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import rasa_sdk.events
from .database import DataFetch, DataInsert, GetPrice

import requests


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="મારી દુનિયા માં તમારું સ્વાગત છે")

        return []


class ActionRestaurant(Action):

    def name(self) -> Text:
        return "action_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'hotel':
                name = e['value']
                print(name)
            if name == 'ભારતીય':
                message = 'ભારતીય રેસ્ટોરન્ટ'
            if name == 'ચાઇનીઝ':
                message = 'ચાઇનીઝ રેસ્ટોરન્ટ'
            if name == 'થાઇ':
                message = 'થાઇ રેસ્ટોરન્ટ'
            if name == 'ઇટાલિયન':
                message = 'ઇટાલિયન રેસ્ટોરન્ટ'
        print(message)

        dispatcher.utter_message(text=message)

        return []


class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get(
            "https://api.covid19india.org/data.json").json()
        entities = tracker.latest_message['entities']
        print(entities)
        state = None
        for e in entities:
            if e['entity'] == 'state':
                state = e['value']

        if state == 'ગુજરાત':
            state = 'gujarat'
        if state == 'રાજસ્થાન':
            state = 'rajasthan'
        if state == 'માધ્યાપ્રદેશ':
            state = 'madhya pradesh'
        if state == 'મહારાષ્ટ્ર':
            state = 'maharashtra'
        confirmed_cases = ''
        for data in response["statewise"]:
            if data["state"] == state.title():
                confirmed_cases = data['confirmed']
                print(data)
                break
        message = state + ": \nConfirmed Cases: " + confirmed_cases
        dispatcher.utter_message(text=message)

        return []


class ActionPlantProtect(Action):

    def name(self) -> Text:
        return "action_plant_protection_solution"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        print(entities)       

        plant_name = ''
        plant_problem = ''
        plant_area = ''
        print(entities)
        for e in entities:
            if e['entity']=='plant_name':
                plant_name = e['value']
            if e['entity']=='plant_problem':
                plant_problem = e['value']
            if e['entity']=='plant_area':
                plant_area=e['value']


        message = ''
        if plant_name == '' and plant_problem == '':
            message += "કૃપયા કરી પાક અને સમસ્યા નું નામ જણાવજો"
        elif plant_name == '':
                message += "કૃપયા કરી પાક નું નામ જણાવો"
        elif plant_problem == '':
                message += "કૃપયા કરી તમારી સમસ્યા જણાવો"


        if (plant_name != '' and plant_problem != '') or plant_area!='':
            if plant_area != '':
                message = 'અનાજના નામ:' + plant_name + ', સમસ્યાનું નામ:' + plant_problem + ' ભાગ: ' + plant_area + '\n'
            else:
                message = 'અનાજના નામ:' + plant_name + ', સમસ્યાનું નામ:' + plant_problem + '\n'
            result = DataFetch(plant_name, plant_area, plant_problem)
            if result != None:
                message += result[0]                
            else:
                message += "માફ કરજો, અત્યારે આ જાણકારી અમારી પાસે નથી"
            

        dispatcher.utter_message(text=message)

        return []

class ActionPleaseRephrase(Action):    
        def name(self) -> Text:
            return "action_please_rephrase"
    
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            query = tracker.latest_message['text']
            print(query)

            DataInsert(query)

            message = "માફ કરશો, હું તે વિનંતીને સંભાળી શકતો નથી."
            dispatcher.utter_message(text=message)
    
            return []

class ActionPlantPrice(Action):

    def name(self) -> Text:
        return "action_plant_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        print(entities)       

        plant_name = ''        
        print(entities)
        for e in entities:
            if e['entity']=='plant_name':
                plant_name = e['value']

        message = ''
        if plant_name == '':                    
            message += "કૃપયા કરી પાક નું નામ જણાવો"
        else:            
            message = 'અનાજના નામ:' + plant_name + '\n'
            result = GetPrice(plant_name)
            if result != None:
                message += result[0]
            else:
                message += "માફ કરજો, અત્યારે આ જાણકારી અમારી પાસે નથી"
            

        dispatcher.utter_message(text=message)

        return []            
