import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from src.utils.logger import logger

class TelegramPublisher:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHANNEL_ID
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def publish(self, message: str) -> bool:
        if not self.token or not self.chat_id:
            logger.warning("Telegram credentials missing. Skipping publish.")
            print(f"[PREVIEW TELEGRAM MESSAGE]:\n{message}\n")
            return False

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Published to Telegram successfully.")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to publish to Telegram: {e}")
            return False
