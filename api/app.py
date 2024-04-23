from fastapi import FastAPI
from pydantic import BaseModel
import call_pods

class Bot(BaseModel):
    key_instance: str

app = FastAPI()

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
    call_pods.api_instance.delete_namespaced_pod(name=pod_id,namespace="default")
    for index, bot in enumerate(bots):
        if bot["pod_id"] == pod_id:
            del bots[index]
            return  f"bot {pod_id} eliminado exitosamente"

@app.delete("/delete_all_bots/")
async def delete_bots():
    pods = call_pods.api_instance.list_namespaced_pod(namespace="default")
    for pod in pods.items:
        call_pods.api_instance.delete_namespaced_pod(name=pod.metadata.name, namespace="default")
    bots.clear()
    return "deleted pods"
async def update_bots():
    pass
