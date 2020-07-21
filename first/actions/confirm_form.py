from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pymongo
from pymongo import MongoClient
from rasa_sdk.events import SlotSet, FollowupAction
import pymongo


class ActionFindMongo(Action):

    def name(self) -> Text:
        return "action_confirm_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:




        return []
