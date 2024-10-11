import os
import string
from collections import Counter
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.db import connections

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    nltk.download('stopwords')
    nltk.download('punkt')
    logging.info("NLTK data downloaded successfully.")
except Exception as e:
    logging.error(f"Error downloading NLTK data: {e}")

class APIClient:

    def clean_text(self, text, key):
        additional_chars = '»«–‘’'
        additional_words = ['2024', '2025', 'directo', 'tras', 'hoy', '’', '‘']
        
        cleaned_text = ''.join([char.lower() for char in text if char not in string.punctuation + additional_chars + '“”'])
        words = [word for word in cleaned_text.split() if word not in additional_words and word != key.lower()]
        
        return ' '.join(words)

    def process_titles(self, json_list, language="en", key=""):
        lang_map = {"es": "spanish", "en": "english"}
        if language not in lang_map:
            raise ValueError("Language not supported.")
        
        stop_words = set(stopwords.words(lang_map[language]))
        word_freq = Counter()
        
        for json_obj in json_list:
            title = json_obj.get('title', '')
            cleaned_title = self.clean_text(title, key)
            word_tokens = word_tokenize(cleaned_title, language=lang_map[language])
            
            for word in word_tokens:
                if word.lower() not in stop_words:
                    word_freq[word.lower()] += 1
        
        return [{'word': word, 'frequency': freq} for word, freq in word_freq.most_common(40)]

    def _fetch_all_as_dict(self, cursor):
        columns = [col[0] for col in cursor.description]  # Get column names
        return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Create dict for each row

    def more_frequent_word(self, key_instance, interval='1D', language="en", country="US"):
        time_interval = self._get_time_interval(interval)
        query = """
            SELECT title FROM newsdropbd.news
            WHERE key_str = %s AND published_date >= NOW() - INTERVAL {0}
            AND language = %s AND country = %s
            ORDER BY published_date DESC;
        """.format(time_interval)

        with connections['APP'].cursor() as cursor:
            try:
                cursor.execute(query, (key_instance, language, country))
                result = self._fetch_all_as_dict(cursor)
                return self.process_titles(result, language=language, key=key_instance)
            except Exception as e:
                logging.error(f"Error retrieving frequent words: {e}")

    def sentiment(self, key_instance, language="en", country="US"):
        query = """
            WITH LatestRecords AS (
                SELECT DATE_FORMAT(published_date, '%Y-%m-%d') AS day,
                AVG(sentiment_score) AS avg_score,
                AVG(sentiment_magnitude) AS avg_magnitude
                FROM newsdropbd.news
                WHERE key_str = %s AND language = %s AND country = %s
                GROUP BY DATE_FORMAT(published_date, '%Y-%m-%d')
                ORDER BY day DESC LIMIT 7
            )
            SELECT day, avg_score, avg_magnitude
            FROM LatestRecords ORDER BY day ASC;
        """
        
        with connections['APP'].cursor() as cursor:
            try:
                cursor.execute(query, (key_instance, language, country))
                result = self._fetch_all_as_dict(cursor)
                logging.info("Sentiment data retrieved successfully.")
                return result
            except Exception as e:
                logging.error(f"Error retrieving sentiment data: {e}")


    def get_news_frequency(self, key_instance, interval='1D', language="en", country="US"):
        time_interval = self._get_time_interval(interval)
        query = """
            SELECT DATE_FORMAT(published_date, '%Y-%m-%d %H:00:00') AS interval_published,
            COUNT(*) AS count_per_interval
            FROM newsdropbd.news
            WHERE key_str = %s AND published_date >= NOW() - INTERVAL {0}
            AND language = %s AND country = %s
            GROUP BY interval_published ORDER BY interval_published;
        """.format(time_interval)

        with connections['APP'].cursor() as cursor:
            try:
                cursor.execute(query, (key_instance, language, country))
                result = self._fetch_all_as_dict(cursor)
                logging.info("News frequency data retrieved successfully.")
                return result
            except Exception as e:
                logging.error(f"Error retrieving news frequency: {e}")

    def most_frequent_time(self, key_instance, interval='1D', language="en", country="US"):
        time_interval = self._get_time_interval(interval)
        query = """
            WITH news_stats AS (
                SELECT DATE_FORMAT(published_date, '%m-%d %H:00:00') AS interval_published,
                COUNT(*) AS count_per_interval,
                (SELECT COUNT(*) FROM newsdropbd.news WHERE key_str = %s) AS total_news,
                DATE_FORMAT(published_date, '%H:00:00') AS hour_only
                FROM newsdropbd.news
                WHERE key_str = %s AND published_date >= NOW() - INTERVAL {0}
                AND language = %s AND country = %s
                GROUP BY interval_published, hour_only
            )
            SELECT interval_published, count_per_interval,
            CONCAT(ROUND((count_per_interval / total_news) * 100, 2), '%') AS percent_total,
            ROUND(AVG(count_per_interval) OVER (PARTITION BY hour_only), 2) AS avg_per_day,
            ROUND(MAX(count_per_interval) OVER (PARTITION BY hour_only), 2) AS max_per_day,
            ROUND(MIN(count_per_interval) OVER (PARTITION BY hour_only), 2) AS min_per_day,
            ROUND(STDDEV(count_per_interval) OVER (PARTITION BY hour_only), 2) AS stddev_per_day
            FROM news_stats ORDER BY count_per_interval DESC LIMIT 5;
        """.format(time_interval)

        with connections['APP'].cursor() as cursor:
            try:
                cursor.execute(query, (key_instance, key_instance, language, country))
                result = self._fetch_all_as_dict(cursor)
                logging.info("Most frequent time data retrieved successfully.")
                return result
            except Exception as e:
                logging.error(f"Error retrieving most frequent time: {e}")

    def news_by_key(self, key_instance, language="en", country="US"):
        query = "SELECT * FROM newsdropbd.news WHERE key_str = %s AND language = %s AND country = %s ORDER BY published_date DESC LIMIT 4"
        
        with connections['APP'].cursor() as cursor:
            try:
                cursor.execute(query, (key_instance, language, country))
                result = self._fetch_all_as_dict(cursor)
                return result
            except Exception as e:
                logging.error(f"Error retrieving news by key: {e}")

    def _get_time_interval(self, interval):
        intervals = {'1D': '1 DAY', '7D': '7 DAY', '1M': '30 DAY'}
        return intervals.get(interval, '1 DAY')
