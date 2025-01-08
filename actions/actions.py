# import hitung mtk
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sympy import sympify
import re
# import cuaca
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
# import textblob
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from textblob import TextBlob

# hitung mtk
class ActionCalculate(Action):

    def name(self) -> Text:
        return "action_calculate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Ambil ekspresi dari user input
        user_message = tracker.latest_message['text']
        match = re.search(r'\d+(\s*[\+\-\*/]\s*\d+)+', user_message)

        if match:
            expression = match.group(0)
            try:
                # Hitung hasil ekspresi
                # result = eval(expression)
                # response = f"Hasil dari perhitungan {expression} adalah {result}"
                result = sympify(expression)
                response = f"Hasil dari perhitungan {expression} adalah {result}"
            except Exception as e:
                response = "Maaf, saya tidak bisa menghitung itu."
        else:
            response = "Saya tidak menemukan perhitungan yang valid di input Tuan."

        dispatcher.utter_message(text=response)
        return []

# cuaca
class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Ambil lokasi dari entitas
        location = next(tracker.get_latest_entity_values("location"), None)

        if location:
            api_key = "your api key"  # Ganti dengan API Key OpenWeatherMap Anda
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]

                response_message = (f"Cuaca di {location} saat ini adalah {description} "
                                    f"dengan suhu {temperature}°C.")
            else:
                response_message = f"Maaf, saya tidak dapat menemukan informasi cuaca untuk {location}."
        else:
            response_message = "Silakan sebutkan lokasi yang ingin Tuan ketahui cuacanya."

        dispatcher.utter_message(text=response_message)
        return []

# textblob
class ActionAnalyzeSentiment(Action):
    def name(self) -> str:
        return "action_analyze_sentiment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[str, Any]):
        user_message = tracker.latest_message.get('text')
        analysis = TextBlob(user_message)
        sentiment = analysis.sentiment.polarity

        if sentiment > 0:
            sentiment_result = "positif"
        elif sentiment < 0:
            sentiment_result = "negatif"
        else:
            sentiment_result = "netral"

        dispatcher.utter_message(text=f"Saya mendeteksi sentimen Anda sebagai {sentiment_result}.")
        return []