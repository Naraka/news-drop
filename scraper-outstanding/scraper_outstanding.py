import feedparser
import time
import os
import mysql.connector
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Really Simple Syndication, Atom
RSS_URL = "https://news.google.com/rss"

class News:

    def __init__(self, language="es", country="ES"):
        self.language = language
        self.country = country

    def get_drops(self):
        self._url = "{}?hl={}&gl={}&ceid={}:{}".format(RSS_URL,
                                                       self.language,
                                                       self.country,
                                                       self.country,
                                                       self.language)
        return self._get_feeds(self._url)

    def _get_feeds(self, url: str):
        feeds = feedparser.parse(url)
        serialized_feeds = list(map(self._serialization, feeds.entries))
        return serialized_feeds

    def _serialization(self, entrie):
        json = {
            "title": self._title_clean(entrie.title),
            "link": entrie.link,
            "published_date": self._published_date_clean(entrie.published),
            "description": self._description_clean(entrie.description),
            "source": entrie.source.title,
            "key_str": "outstanding",
            "language": self.language,
            "country": self.country,
        }
        return json

    def _published_date_clean(self, published_date):
        ptime = datetime.strptime(published_date, '%a, %d %b %Y %H:%M:%S %Z')
        return ptime.strftime('%Y-%m-%d %H:%M:%S')

    def _description_clean(self, description):
        start = description.find('<a')
        end = description.find('</a>')

        if start != -1 and end != -1:
            description_tags = description[start:end]
            first_gt = description_tags.find('>')
            if first_gt != -1:
                clean_text = description_tags[first_gt + 1:]
                return clean_text
        return None

    def _title_clean(self, title):
        index_hyphen = title.rfind('-')
        if index_hyphen != -1:
            return title[:index_hyphen].strip()
        else:
            return title.strip()

    def listening_drops(self):
        try:
            DB_USER = os.environ.get('DB_USER')
            DB_PASSWORD = os.environ.get('DB_PASSWORD')
            DB_NAME = os.environ.get('DB_NAME')
            UNIX_SOCKET_PATH = f"/cloudsql/{os.environ.get('INSTANCE_CONNECTION_NAME')}"
            logging.info("Database credentials have been assigned successfully.")
        except Exception as e:
            logging.error(f"Failed to assign database credentials: {e}")
            return

        try:
            conn = mysql.connector.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                unix_socket=UNIX_SOCKET_PATH
            )
            logging.info("Successfully connected to the database.")
        except mysql.connector.Error as err:
            logging.error(f"Error connecting to the database: {err}")
            return

        cursor = conn.cursor()

        for _ in range(3):
            batch = self.get_drops()
            for entrie in batch:
                cursor.execute("""
                    SELECT * FROM news 
                    WHERE title = %s 
                    AND link = %s 
                    AND published_date = %s 
                    AND description = %s 
                    AND source = %s 
                    AND key_str = %s
                    AND language = %s
                    AND country = %s
                """, (
                    entrie["title"],
                    entrie["link"],
                    entrie["published_date"],
                    entrie["description"],
                    entrie["source"],
                    entrie["key_str"],
                    entrie["language"],
                    entrie["country"]
                ))
                existing_row = cursor.fetchone()

                if existing_row:
                    logging.info("The complete row already exists in the database. No insertion will occur.")
                else:
                    cursor.execute("""
                        INSERT INTO news (title, link, published_date, description, source, key_str, language, country)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        entrie["title"],
                        entrie["link"],
                        entrie["published_date"],
                        entrie["description"],
                        entrie["source"],
                        entrie["key_str"],
                        entrie["language"],
                        entrie["country"]
                    ))
                    conn.commit()
                    logging.info("New entry inserted into the database.")

            time.sleep(200)  # Delay before the next iteration

        cursor.close()
        conn.close()
        logging.info("Database connection closed after processing.")
