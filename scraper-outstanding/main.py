from scraper_outstanding import News
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    load_dotenv()
    logging.info("Environment variables loaded successfully")
except Exception as e:
    logging.error("Failed to load environment variables: %s", e)

language = os.environ.get("language")
country = os.environ.get("country")

if language and country:
    try:
        feed = News(language=language, country=country)
        logging.info("News instance created with language: %s and country: %s", language, country)
        feed.listening_drops()
    except Exception as e:
        logging.error("Failed to initialize News or start listening: %s", e)
else:
    logging.error("Language or country environment variable is missing.")
