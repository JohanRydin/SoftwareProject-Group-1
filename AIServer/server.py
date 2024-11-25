from fastapi import FastAPI
from main import get_recommendations

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/recommendations")
def read_recommendations(body: dict):
    user_data = body.get("user")
    rows_data = body.get("rows")

    # Validate the data manually (if needed)
    if not user_data or not rows_data:
        return {"error": "Missing required data"}

    recommendations = get_recommendations(user_data, rows_data)

    return {"games": ["CS2", "Baldurs Gate 3"], "user_id":user_data['id']}
