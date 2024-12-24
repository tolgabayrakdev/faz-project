from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .controller import auth_controller


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth_controller.router, prefix="/api/auth")


@app.get("/")
async def root():
    return {"message": "Hello World"}
