from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Music Recommendation System is Running!"}

@app.get("/recommend")
def recommend(song: str, artist: str):
    db = [
        {"title": "Hype Boy", "artist": "NewJeans", "link": "https://music.youtube.com/watch?v=11cta61wi0g"},
        {"title": "Ditto", "artist": "NewJeans", "link": "https://music.youtube.com/watch?v=pSUydWEqKwE"},
        {"title": "To. X", "artist": "Taeyeon", "link": "https://music.youtube.com/watch?v=vJ3pOfT8S0I"}
    ]
    return {"input": f"{song} - {artist}", "recommendation": random.choice(db)}