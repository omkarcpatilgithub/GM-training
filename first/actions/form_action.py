
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
import pymongo
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, FollowupAction
import re

class FacilityForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "action_form_ask_name"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        
        return ["name", "email"]

## how is this returning form intent
    ## got it, check nlu.md once

    def slot_mappings(self) -> Dict[Text, Any]:
        # return {"name": self.from_entity(entity="name",
        #                                  intent=["name"]),

        print('taking name and email')
        return {"name": [self.from_text(intent=["name"])],
                "email": [self.from_text(intent=["email"])]}
   
    def validate_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""


        print('########################################3')
        print(tracker.slots)
        print('########################################3')
        # print(tracker.latest_message)


        print(tracker.latest_action_name)
        if (tracker.slots['name']):
            value = tracker.slots['name']
        print('returning whole value')
        return {"name": value}

    def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        print(tracker.slots)
        pattern = '^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'

        if(re.match(pattern, value)):
            return {"email": value}
        else:
            dispatcher.utter_template("utter_ask_email", tracker)
            return {"email": None}



        # if len(value) > 2:
        #     sender_id = tracker.sender_id
        #     slotStorage.set_slot(sender_id, "name", value)
        #     return {"name": value}
        # else:
        #     dispatcher.utter_template("utter_ask_name", tracker)
        #     return {"name": None}
        

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')

        ## connecting to mongo db
        link = 'mongodb://localhost:27017'
        cluster = MongoClient(link)
        db = cluster["rasa"]
        collection = db["rasa"]

        print(tracker.sender_id, name, email)

        ## inserting to db
        post = {"session": tracker.sender_id, "name": name, "email": email}
        collection.insert_one(post)

        dispatcher.utter_message(text="cool now you are registered, Hello {}, tell me how can i help you".format(name))

        return [FollowupAction("actions_find_in_mongo")]
        # return [FollowupAction("action_confirm_form")]



