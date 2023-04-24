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
import csv
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class StoreCovidStatusAction(Action):
    def name(self) -> Text:
        return "action_store_covid_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve the slot values
        student_id = tracker.get_slot("student_id")
        status = tracker.get_slot("status")
        test_type = tracker.get_slot("test_type")

        # Write to CSV file
        with open("storage/covid_status.csv", mode="a") as f:
            writer = csv.writer(f)
            writer.writerow([student_id, status, test_type])

        # Send a message to the user confirming that the information was stored
        dispatcher.utter_message(text="Thank you for providing your COVID test result. Your information has been recorded.")

        return []

class FindStudentIdAction(Action):
    def name(self) -> Text:
        return "action_find_student_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve the student's first name and last name
        first_name = tracker.slots.get("first_name")
        last_name = tracker.slots.get("last_name")

        # Search for the student id in the CSV file
        if first_name and last_name:
          if not os.path.exists("storage"):
            os.mkdir("storage")
          if not os.path.exists(b"storage/students.csv"): 
            ## if file does not exist, copy from storage_file_format
            with open("storage_file_format/students.csv", mode="r", encoding='utf-8-sig') as read_file:
              with open("storage/students.csv", mode="w", encoding='utf-8-sig') as write_file:
                write_file.write(read_file.read())

          with open("storage/students.csv", mode="r", encoding='utf-8-sig') as f:
              reader = csv.DictReader(f)
              for row in reader:
                  if row["first_name"] == first_name and row["last_name"] == last_name:
                      student_id = row["student_id"]
                      dispatcher.utter_message(text=f"Your student ID is {student_id}")
                      return [SlotSet("student_id", student_id)]

          
          # If the student is not found in the CSV file, notify the user
        dispatcher.utter_message(text="Sorry, I could not find your student ID. Please contact your school administrator for assistance.")
        return [SlotSet("student_id", None)]

class RespondTest(Action):
  def __init__(self):
    super().__init__()
    self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

  def name(self) -> Text:
    return "action_utter_chitchat"
  
  def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    message = tracker.latest_message("text")
    new_user_input_ids = tokenizer.encode(input(">> User:") + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    dispatcher.utter_message(text=response)
    return []
