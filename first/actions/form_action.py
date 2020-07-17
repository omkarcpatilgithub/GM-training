
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
import pymongo
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, FollowupAction

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
        return {"name": [self.from_text()],
                "email": self.from_entity(entity="email",
                                             # intent="inform")}
                                             intent=["email"])}


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

        #dispatcher.utter_message(text="cool now you are registered, Hello {}, tell me how can i help you".format(name))

        return [FollowupAction("actions_find_in_mongo")]



