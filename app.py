from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Sharkflow!"}

@app.get("/health")
def health():
    return {"ok": True}
