from google.cloud import language_v2
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import time

def analyze(news):
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(
        content=news, type_=language_v2.Document.Type.PLAIN_TEXT
    )
    return client.analyze_sentiment(request={"document": document})

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
    
def add_sentiment():
    connection = create_connection()
    if not connection:
        raise "Error connecting to the database"
    
    cursor = connection.cursor(dictionary=True)
    query = """ SELECT * 
                FROM newsdropbd.news 
                ORDER BY id DESC 
                LIMIT 10000;
            """
    
    cursor.execute(query)
    news = cursor.fetchall()

    for new in news:
        if new["sentiment_magnitude"] is None or new ["sentiment_score"] is None:
            data = analyze(new["title"])
            update_query = "UPDATE newsdropbd.news SET sentiment_score = %s, sentiment_magnitude = %s WHERE id = %s;"
            cursor.execute(update_query, (data.document_sentiment.score, data.document_sentiment.magnitude, new["id"]))
            connection.commit()
            time.sleep(20)
        else:
            pass

    cursor.close()
    connection.close()

add_sentiment()