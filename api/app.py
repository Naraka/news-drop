from fastapi import FastAPI
from pydantic import BaseModel
import docker

client = docker.from_env()
docker_image = "news-drop-container:0.1.3"

class Bot(BaseModel):
    instance_key: str

app = FastAPI()

bots = []

@app.get("/")
async def root():
    return "Welcome to news-drop api"

@app.post("/post_bot/")
async def post_bot(instance_key:Bot):
    container = client.containers.run(
        docker_image,
        detach=True,
        environment={"key_instance":instance_key.instance_key},
    )
    bots.append({
        "instance_key":instance_key.instance_key,
        "docker_image":docker_image,
        "container_id":container.id,
        "container_name":container.name,
    })
    return instance_key.instance_key

@app.get("/get_bots/")
async def get_bots():
    return bots

@app.delete("/delete_bots/{container_id}")
async def delete_bots(container_id:str):
    client.containers.get(container_id).stop()
    for index, bot in enumerate(bots):
        if bot["container_id"] == container_id:
            del bots[index]
            return  f"bot {container_id} eliminado exitosamente"

async def update_bots():
    pass
