import requests
import base64
from config.settings import BLOG_API_URL, BLOG_USERNAME, BLOG_PASSWORD
from src.utils.logger import logger

class BlogPublisher:
    def __init__(self):
        self.api_url = BLOG_API_URL
        self.username = BLOG_USERNAME
        self.password = BLOG_PASSWORD

    def publish(self, title: str, content: str, tags: list = None) -> bool:
        if not self.api_url:
            logger.warning("Blog API URL missing. Skipping publish.")
            # print(f"[PREVIEW BLOG POST]:\nTitle: {title}\nContent: {content[:100]}...\n")
            return False

        # Basic Auth for WordPress Application Password
        creds = f"{self.username}:{self.password}"
        token = base64.b64encode(creds.encode()).decode()
        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "title": title,
            "content": content,
            "status": "publish",
            # "categories": [1], # You'd need to fetch category IDs first
            # "tags": tags      # Tags handling requires IDs in WP usually
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            logger.info(f"Published to Blog: {title}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to publish to blog: {e}")
            if response := e.response:
                logger.error(f"Response: {response.text}")
            return False
