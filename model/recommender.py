import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ytmusicapi import YTMusic
import os

class SongRecommender:
    def __init__(self, dataset_path="model/dataset.csv"):
        self.yt = YTMusic()
        # Load the dataset
        if os.path.exists(dataset_path):
            self.df = pd.read_csv(dataset_path)
            # Create a combined feature string for each song to compute similarity
            self.df['features'] = self.df['title'] + " " + self.df['artist'] + " " + self.df['genre']
            
            # Initialize TF-IDF Vectorizer (lightweight NLP model)
            self.vectorizer = TfidfVectorizer()
            self.tfidf_matrix = self.vectorizer.fit_transform(self.df['features'])
        else:
            self.df = pd.DataFrame()

    def recommend(self, song: str, artist: str, top_n: int = 3):
        if self.df.empty:
            return [{"title": "Error", "artist": "Dataset not found", "link": ""}]

        # Treat input as a query to match against features
        query = f"{song} {artist}"
        query_vec = self.vectorizer.transform([query])
        
        # Compute cosine similarity between user query and dataset
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Get indices of the most similar songs in descending order
        top_indices = sim_scores.argsort()[-top_n:][::-1]
        
        recommendations = []
        for idx in top_indices:
            # Ensure there is at least some text similarity match
            if sim_scores[idx] > 0.01:
                rec_title = self.df.iloc[idx]['title']
                rec_artist = self.df.iloc[idx]['artist']
                
                # Fetch YouTube Music Link dynamically
                search_query = f"{rec_title} {rec_artist}"
                yt_link = self.get_youtube_music_link(search_query)
                
                recommendations.append({
                    "title": rec_title,
                    "artist": rec_artist,
                    "link": yt_link
                })
                
        # Fallback if query was entirely dissimilar to dataset
        if not recommendations:
            return [{"title": "No close match in DB", "artist": "Try another query", "link": ""}]
        
        return recommendations

    def get_youtube_music_link(self, query: str) -> str:
        try:
            results = self.yt.search(query, filter="songs", limit=1)
            if results:
                # Get the first song video ID securely
                video_id = results[0].get('videoId')
                if video_id:
                    return f"https://music.youtube.com/watch?v={video_id}"
        except Exception as e:
            print(f"Error fetching YT link for {query}: {e}")
        return "https://music.youtube.com/"
