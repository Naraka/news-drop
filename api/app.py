from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import call_pods
import os
import mysql.connector
from mysql.connector import Error

app = FastAPI()

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



class Bot(BaseModel):
    key_instance: str


bots = []

@app.get("/")
async def root():
    return "Welcome to news-drop api"

@app.post("/post_bot/")
async def post_bot(key_instance:Bot):
    pod_id = call_pods.crear_pod(key_instance.key_instance)
    bots.append({
        "key_instance":key_instance.key_instance,
        "pod_id":pod_id,
    })
    return key_instance.key_instance

@app.get("/get_bots/")
async def get_bots():
    return bots

@app.delete("/delete_bots/{pod_id}")
async def delete_bots(pod_id:str):
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
