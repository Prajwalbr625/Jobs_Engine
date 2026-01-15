import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "jobs.db"
LOG_FILE = LOG_DIR / "app.log"

# Fetcher Settings
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
REQUEST_TIMEOUT = 10
FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", "15"))

# Telegram Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# Blog Settings
BLOG_API_URL = os.getenv("BLOG_API_URL")
BLOG_USERNAME = os.getenv("BLOG_USERNAME")
BLOG_PASSWORD = os.getenv("BLOG_PASSWORD")

# LinkedIn Settings
# Location Filtering
# Only allow jobs that match at least one of these keywords (Case-insensitive)
# Set to None or empty list to allow ALL locations.
ALLOWED_LOCATIONS = ["India", "Remote", "Bengaluru", "Bangalore", "Delhi", "Mumbai", "Pune", "Hyderabad", "Chennai", "Gurgaon", "Noida"]

# Block jobs that match these keywords
BLOCKED_LOCATIONS = ["United States", "USA", "UK", "London", "Europe", "China"]

