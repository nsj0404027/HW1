from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from model.face_recommender import FaceRecommender
import os
import shutil
import urllib.parse
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="Face Recognition API")
recommender = FaceRecommender()

os.makedirs("static", exist_ok=True)
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

def search_naver_image(query: str):
    """
    Scrapes Naver Integrated Search to find the celebrity's profile image result.
    """
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src and 'search.pstatic.net/common' in src and 'people' in urllib.parse.unquote(src):
                return src
            elif src and 'search.pstatic.net/common' in src: # fallback if people string not found
                return src
    except Exception as e:
        print(f"Error fetching image: {e}")
    # Fallback placeholder
    return "https://via.placeholder.com/300?text=No+Image+Found"

@app.get("/")
def home():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Service is Running!"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...), category: str = Form("all")):
    # Save the file temporarily
    file_path = f"static/uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Predict the celebrity
    result = recommender.recommend(file_path, category)
    celebrity_name = result["name"]
    
    # Fetch the celebrity image from Naver
    celeb_img_url = search_naver_image(celebrity_name)
    
    return {
        "user_image": f"/static/uploads/{file.filename}",
        "celebrity_name": celebrity_name,
        "celebrity_image_url": celeb_img_url,
        "instagram": result["instagram"],
        "namuwiki": result["namuwiki"]
    }