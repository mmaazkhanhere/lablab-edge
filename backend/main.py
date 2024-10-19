from fastapi import FastAPI

app: FastAPI = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}