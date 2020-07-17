from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, FollowupAction
import pymongo


class ActionDeregister(Action):

    def name(self) -> Text:
        return "actions_deregister"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        print(tracker.sender_id)
        session = tracker.sender_id

        link = 'mongodb://localhost:27017'
        cluster = MongoClient(link)
        db = cluster["rasa"]
        collection = db["rasa"]

        results = collection.find({"session": session})
        user = results[0]['name']
        collection.delete_many({"session": session})

        dispatcher.utter_message(text="ok {}, your number is deregistered from our system \n hope to see you again soon".format(user))

        return [SlotSet("name", None), SlotSet("email", None)]
