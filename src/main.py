from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=[
        "http://localhost:3000",
        "https://localhost:3000",
        "http://atom-fit-frontend.vercel.app",
        "https://atom-fit-frontend.vercel.app",
    ],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

for router in routers:
    app.include_router(router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
