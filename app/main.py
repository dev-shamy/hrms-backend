from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db import database
from src.db.database import Base
from src.routes.main import api_router

Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="HRMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/", tags=["root"])
def read_root():
    return {"message": "server is running"}
