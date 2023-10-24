from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.router import router as api_router
from src.db.base import database, engine, metadata

metadata.create_all(engine)

app = FastAPI()


origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(api_router)
