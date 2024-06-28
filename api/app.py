from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import call_pods
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


app = FastAPI()

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
async def get_news_by_key(key: str):
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM newsdropbd.news WHERE key_str = %s ORDER BY published_date DESC LIMIT 10"
    
    try:
        cursor.execute(query, (key,))
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()



class Bot(BaseModel):
    key_instance: str


bots = []

@app.get("/")
async def root():
    return "Welcome to news-drop api"

@app.post("/post_bot/")
async def post_bot(key_instance:Bot):
    if key_instance.key_instance not in [bot['key_instance'] for bot in bots]:
        pod_id = call_pods.crear_pod(key_instance.key_instance)
        bots.append({
            "key_instance":key_instance.key_instance,
            "pod_id":pod_id,
        })
        return key_instance.key_instance
    else:
        return key_instance.key_instance

@app.get("/get_bots/")
async def get_bots():
    return bots

@app.delete("/delete_bots/{key_instance}")
async def delete_bots(key_instance:str):
    for i in bots:
        if i["key_instance"] == key_instance:
            pod_id=i["pod_id"]

    call_pods.api_instance.delete_namespaced_pod(name=pod_id,namespace="api-namescape-news-drop")
    for index, bot in enumerate(bots):
        if bot["pod_id"] == pod_id:
            del bots[index]
            return  f"bot {pod_id} eliminado exitosamente"



@app.delete("/delete_all_bots/")
async def delete_bots():
    pods = call_pods.api_instance.list_namespaced_pod(namespace="api-namescape-news-drop")
    for pod in pods.items:
        call_pods.api_instance.delete_namespaced_pod(name=pod.metadata.name, namespace="api-namescape-news-drop")
    bots.clear()
    return "deleted pods"
async def update_bots():
    pass





@app.get("/get_more_frequent_word/{key}")
async def get_more_frequent_word(key: str):
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    query = """
                SELECT word, COUNT(*) AS frequency
                FROM (
                    SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(title, ' ', n.digit+1), ' ', -1) AS word
                    FROM newsdropbd.news
                    JOIN (
                        SELECT 0 AS digit UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
                        UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7
                        UNION ALL SELECT 8 UNION ALL SELECT 9
                    ) n
                    ON LENGTH(REPLACE(title, ' ', '')) <= LENGTH(title)-n.digit
                    WHERE key_str = %s
                ) words
                GROUP BY word
                ORDER BY frequency DESC
                LIMIT 40;

            """
    
    try:
        cursor.execute(query, (key,))
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()





@app.get("/get_news_frequency/{key}")
async def get_news_frequency(key: str):
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    query = """
                SELECT
                    DATE_FORMAT(published_date, '%Y-%m-%d %H:00:00') AS interval_published,
                    COUNT(*) AS count_per_interval
                FROM
                    newsdropbd.news
                WHERE
                    key_str = %s
                GROUP BY
                    interval_published
                ORDER BY
                    interval_published;
            """
    
    try:
        cursor.execute(query, (key,))
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@app.get("/most_frequent_time/{key}")
async def most_frequent_time(key: str):
    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
    cursor = connection.cursor(dictionary=True)
    query = """
                    SELECT 
                        DATE_FORMAT(published_date, '%H:00:00') AS hour
                    FROM 
                        newsdropbd.news
                    WHERE 
                        key_str = %s
                    GROUP BY 
                        hour
                    ORDER BY 
                        COUNT(*) DESC
                    LIMIT 3;
            """
    
    try:
        cursor.execute(query, (key,))
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()