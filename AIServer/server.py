from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "Hello": "World"}

@app.get("/recommendations")
def get_recommendations():
    return {"games": ["CS2", "Baldurs Gate 3"]}
