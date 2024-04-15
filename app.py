from fastapi import FastAPI
from news_drop.news_drop import News
from pydantic import BaseModel

class Bot(BaseModel):
    instance_key: str

test_bot = News(max_drops=1, period="1h")

app = FastAPI()

bots = []

@app.get("/")
async def root():
    return "Welcome to news-drop api"

@app.post("/post_bot/")
async def post_bot(instance_key:Bot):
    start = test_bot.listening_drops("banco")
    return instance_key

@app.get("/get_bots")
async def get_bots():
    return bots

async def delete_bot():
    pass