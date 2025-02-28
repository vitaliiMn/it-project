import requests

from config import settings

class TelegramBot:
    def __init__(self, token: str, chat_ID: int):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.chat_ID = chat_ID

    def send_message(self, username: str):
        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": self.chat_ID, "text": f"Привет, {username}!"}
        response = requests.post(url, json=payload)
        return response.json() 
    
bot = TelegramBot(settings.TGBOT_TOKEN, settings.CHAT_ID)