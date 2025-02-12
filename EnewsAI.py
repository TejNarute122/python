import streamlit as st
from PIL import Image
import pytesseract
import requests
from pytube import YouTube

# Function to detect text from an image using Tesseract OCR
def detect_text(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        st.error(f"Error detecting text: {e}")
        return None

# NewsAPI and YouTube API keys
NEWS_API_KEY = "d041c94e5d8c40d7a2e2501be43af96f"
YOUTUBE_API_KEY = "AIzaSyBPrCjzNzko5Y7S1TjDwNGTQWbzmqc2PMo"

# Function to fetch news articles using NewsAPI
def fetch_news(query):
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["articles"]
        return None
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return None

# Function to fetch YouTube videos using YouTube Data API
def fetch_youtube_videos(query):
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}&maxResults=5"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["items"]
        return None
    except Exception as e:
        st.error(f"Error fetching YouTube videos: {e}")
        return None

# Streamlit App
st.title("Enews AI")
st.write("Upload a photo to detect the headline and get related news, videos, and articles.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    # Save the uploaded file
    with open("uploaded_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Detect headline from the image
    headline = detect_text("uploaded_image.jpg")
    if headline:
        st.success(f"Detected Headline: {headline}")
        
        # Fetch related news articles
        st.subheader("Today's Breaking News")
        articles = fetch_news(headline)
        if articles:
            for article in articles[:5]:  # Display top 5 articles
                st.write(f"**{article['title']}**")
                st.write(f"Source: {article['source']['name']}")
                st.write(f"Description: {article['description']}")
                st.write(f"[Read more]({article['url']})")
                st.write("---")
        else:
            st.error("No news articles found.")
        
        # Fetch related YouTube videos
        st.subheader("Related YouTube Videos")
        videos = fetch_youtube_videos(headline)
        if videos:
            for video in videos:
                video_id = video["id"]["videoId"]
                video_title = video["snippet"]["title"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                st.write(f"**{video_title}**")
                st.video(video_url)
        else:
            st.error("No YouTube videos found.")
        
        # Fetch historical news (optional)
        st.subheader("Historical News")
        historical_articles = fetch_news(headline + " history")
        if historical_articles:
            for article in historical_articles[:5]:  # Display top 5 historical articles
                st.write(f"**{article['title']}**")
                st.write(f"Source: {article['source']['name']}")
                st.write(f"Description: {article['description']}")
                st.write(f"[Read more]({article['url']})")
                st.write("---")
        else:
            st.error("No historical news found.")
    else:
        st.error("No text detected in the image.")