from fastapi import FastAPI
from api.routers import routers
app = FastAPI()

for router in routers:
    app.include_router(router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
