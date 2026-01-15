import requests
from abc import ABC, abstractmethod
from fake_useragent import UserAgent
from config.settings import USER_AGENT, REQUEST_TIMEOUT
from src.utils.logger import logger
from src.models import Job
from typing import List

class BaseFetcher(ABC):
    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.ua = UserAgent()
        
    def _get_headers(self):
        return {
            "User-Agent": self.ua.random
        }

    def fetch_page(self, url: str):
        try:
            # SSL verification disabled for local dev environment compatibility
            response = requests.get(url, headers=self._get_headers(), timeout=REQUEST_TIMEOUT, verify=False)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    @abstractmethod
    def fetch_jobs(self) -> List[Job]:
        """
        Must implement this method to return a list of Job objects.
        """
        pass
