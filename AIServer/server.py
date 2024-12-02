from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommendations import Recommender

app = FastAPI()

origins = [
    "http://localhost:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

recommender = Recommender(100)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/recommendations")
def read_recommendations(body: dict):
    user_data = body.get("user")
    rows_data = body.get("rows")

    # Validate the data manually (if needed)
    if not user_data:
        return {"error": "Missing required data"}
    # Default option if there is no rows in the request. Should only happen the first time a user logs in
    if not rows_data:
        rows_data = [{'similar_to_games':'all'}, {'similar_to_genre': None}, {'best_reviewed': None}, {'best_sales': None}]

    recommendations = recommender.get_recommendations(user_data, rows_data)

    return {"games": recommendations}
