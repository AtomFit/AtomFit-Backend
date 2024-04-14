from fastapi import FastAPI
from api.routers import routers
app = FastAPI()

for router in routers:
    app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
