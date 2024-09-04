from contextlib import asynccontextmanager
import string
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import call_pods
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from call_pods import client
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from collections.abc import AsyncIterator

CACHE_EXPIRE = 60 * 10

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
redis_url = f"redis://{redis_host}:{redis_port}"

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

try:
    load_dotenv()
except: pass
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None


@app.get("/news")
@cache(expire=CACHE_EXPIRE)
async def get_news():
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM news"
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()



@app.get("/news/{key}")
@cache(expire=CACHE_EXPIRE)
async def get_news_by_key(key: str, language: str = "en", country:str = "US"):
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM newsdropbd.news WHERE key_str = %s AND language = %s AND country = %s ORDER BY published_date DESC LIMIT 4"
    
    try:
        cursor.execute(query, (key, language, country,))
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()



class Bot(BaseModel):
    key_instance: str
    language: str
    country: str


bots = []

@app.get("/")
async def root():
    return "Welcome to news-drop api"

@app.post("/post_bot/")
async def post_bot(key_instance:Bot):
    if key_instance.key_instance not in [bot['key_instance'] for bot in bots]:
        deployment_name = call_pods.create_deployment(key_instance=key_instance.key_instance, language=key_instance.language, country=key_instance.country)
        bots.append({
            "key_instance":key_instance.key_instance,
            "deployment_name":deployment_name,
        })
        return key_instance.key_instance
    else:
        return key_instance.key_instance

@app.get("/get_bots/")
async def get_bots():
    return bots

@app.delete("/delete_bots/{key_instance}")
async def delete_bots(key_instance: str):
    deployment_name = None

    for index, bot in enumerate(bots):
        if bot["key_instance"] == key_instance:
            deployment_name = bot["deployment_name"]
            break
    
    if not deployment_name:
        raise HTTPException(status_code=404, detail=f"No bot found with key_instance {key_instance}")

    try:
        call_pods.api_instance.delete_namespaced_deployment(name=deployment_name, namespace="bots", body=client.V1DeleteOptions())
    except client.exceptions.ApiException as e:
        raise HTTPException(status_code=e.status, detail=f"Failed to delete Deployment: {e.reason}")

    for index, bot in enumerate(bots):
        if bot["deployment_name"] == deployment_name:
            del bots[index]
            return f"Deployment {deployment_name} eliminado exitosamente"

    raise HTTPException(status_code=500, detail="Deployment not found in the bots list after deletion")



nltk.download('stopwords')
nltk.download('punkt')

def clean_text(text, key):
    additional_chars = '»«–‘’'
    additional_words = ['2024', 'directo', 'tras', 'hoy', '’', '‘']
    
    cleaned_text = ''.join([char.lower() for char in text if char not in string.punctuation + additional_chars + '“”'])
    
    cleaned_text = ' '.join(cleaned_text.split())
    
    words = cleaned_text.split()
    words = [word for word in words if word not in additional_words and word != key.lower()]
    
    cleaned_text = ' '.join(words)
    
    return cleaned_text

def process_titles(json_list, language: str = "en", key: str = ""):
    if language == "es":
        language = "spanish"
    elif language == "en":
        language = "english"
    else:
        raise ValueError("language not assigned")
    
    stop_words = set(stopwords.words(language))
    word_freq = Counter()

    for json_obj in json_list:
        title = json_obj.get('title', '')
        
        cleaned_title = clean_text(title, key)
        
        word_tokens = word_tokenize(cleaned_title, language=language)
        
        for word in word_tokens:
            if word.lower() not in stop_words:
                word_freq[word.lower()] += 1
    
    most_common_words = word_freq.most_common(40)
    
    result_list = [{'word': word, 'frequency': freq} for word, freq in most_common_words]
    
    return result_list


@app.get("/get_more_frequent_word/{key}")
@cache(expire=CACHE_EXPIRE)
async def get_more_frequent_word(key: str, interval: str = '1D', language: str = "en", country:str = "US"):
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    
    if interval == '1D':
        time_interval = 'INTERVAL 1 DAY'
    elif interval == '7D':
        time_interval = 'INTERVAL 7 DAY'
    elif interval == '1M':
        time_interval = 'INTERVAL 30 DAY'
    else:
        raise HTTPException(status_code=400, detail="Interval parameter must be '1day', '7days', or '30days'")
    
    query = f"""
        SELECT title
        FROM newsdropbd.news
        WHERE key_str = %s
        AND published_date >= NOW() - {time_interval}
        AND language = %s
        AND country = %s
        ORDER BY published_date DESC;
    """

    try:
        cursor.execute(query, (key, language, country,))
        result = cursor.fetchall()
        return process_titles(result, language=language, key=key)
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()





@app.get("/get_news_frequency/{key}")
@cache(expire=CACHE_EXPIRE)
async def get_news_frequency(key: str, interval: str = '1D', language: str = "en", country:str = "US"):
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    
    if interval == '1D':
        time_interval = 'INTERVAL 1 DAY'
    elif interval == '7D':
        time_interval = 'INTERVAL 7 DAY'
    elif interval == '1M':
        time_interval = 'INTERVAL 30 DAY'
    else:
        raise HTTPException(status_code=400, detail="Interval parameter must be '1day', '7days', or '30days'")
    query = f"""
                SELECT
                    DATE_FORMAT(published_date, '%Y-%m-%d %H:00:00') AS interval_published,
                    COUNT(*) AS count_per_interval
                FROM
                    newsdropbd.news
                WHERE
                    key_str = %s
                    AND published_date >= NOW() - {time_interval}
                    AND language = %s
                    AND country = %s
                GROUP BY
                    interval_published
                ORDER BY
                    interval_published;
            """
    
    try:
        cursor.execute(query, (key, language, country,))
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@app.get("/most_frequent_time/{key}")
@cache(expire=CACHE_EXPIRE)
async def most_frequent_time(key: str, interval: str = '1D', language: str = "en", country:str = "US"):
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    
    if interval == '1D':
        time_interval = 'INTERVAL 1 DAY'
    elif interval == '7D':
        time_interval = 'INTERVAL 7 DAY'
    elif interval == '1M':
        time_interval = 'INTERVAL 30 DAY'
    else:
        raise HTTPException(status_code=400, detail="Interval parameter must be '1day', '7days', or '30days'")
    
    query = f"""
        WITH news_stats AS (
            SELECT
                DATE_FORMAT(published_date, '%m-%d %H:00:00') AS interval_published,
                COUNT(*) AS count_per_interval,
                (SELECT COUNT(*) FROM newsdropbd.news WHERE key_str = %s) AS total_news,
                DATE_FORMAT(published_date, '%H:00:00') AS hour_only
            FROM
                newsdropbd.news
            WHERE
                key_str = %s
                AND published_date >= NOW() - {time_interval}
                AND language = %s
                AND country = %s
            GROUP BY
                interval_published,
                hour_only
        )
        SELECT
            interval_published,
            count_per_interval,
            CONCAT(ROUND((count_per_interval / total_news) * 100, 2), '%') AS percent_total,
            ROUND(AVG(count_per_interval) OVER (PARTITION BY hour_only), 2) AS avg_per_day,
            ROUND(MAX(count_per_interval) OVER (PARTITION BY hour_only), 2) AS max_per_day,
            ROUND(MIN(count_per_interval) OVER (PARTITION BY hour_only), 2) AS min_per_day,
            ROUND(STDDEV(count_per_interval) OVER (PARTITION BY hour_only), 2) AS stddev_per_day
        FROM
            news_stats
        ORDER BY
            count_per_interval DESC
        LIMIT
            5;
    """
    
    try:
        cursor.execute(query, (key, key, language, country,))
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@app.get("/sentiment/{key}")
@cache(expire=CACHE_EXPIRE)
async def sentiment(key: str, language: str = "en", country:str = "US"):
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    
    query = """
                WITH LatestRecords AS (
                    SELECT
                        DATE_FORMAT(published_date, '%Y-%m-%d') AS day,
                        AVG(sentiment_score) AS avg_score,
                        AVG(sentiment_magnitude) AS avg_magnitude
                    FROM
                        newsdropbd.news
                    WHERE
                        key_str = %s
                        AND language = %s
                        AND country = %s
                    GROUP BY
                        DATE_FORMAT(published_date, '%Y-%m-%d')
                    ORDER BY
                        day DESC
                    LIMIT 7
                )
                SELECT
                    day,
                    avg_score,
                    avg_magnitude
                FROM
                    LatestRecords
                ORDER BY
                    day ASC;
    """
    
    try:
        cursor.execute(query, (key, language, country,))
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()