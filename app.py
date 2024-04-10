from fastapi import FastAPI
from news_drop import News

app = FastAPI()

bot = News(max_drops=10, period="1h")
db = []

@app.post("/create_instance/{instance_key}")
def create_instance(instance_key:str):


    bot.listening_drops(data_set=db, data=instance_key)

    return {"instance_key": instance_key }