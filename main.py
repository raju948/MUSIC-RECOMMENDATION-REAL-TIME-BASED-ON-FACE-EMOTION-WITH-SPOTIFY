import streamlit as st
import cv2
from rmn import RMN
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize RMN model
m = RMN()

# Spotify credentials
SPOTIFY_CLIENT_ID = 'f6026d550b184448b0ca736ecc6f339e'
SPOTIFY_CLIENT_SECRET = 'f540ddb5625d429c961721268b673192'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                           client_secret=SPOTIFY_CLIENT_SECRET))

# Function to detect emotion for a single frame
def detect_emotion(image):
    results = m.detect_emotion_for_single_frame(image)
    return results

# Function to draw detected emotions on the image
def draw_emotions(image, results):
    image = m.draw(image, results)
    return image

def recommend_songs(expression, language):
    recommendations = []
    limit = 10  # Number of songs to recommend
    
    query = f'mood:{expression}'

    if language == "english":
        query += ' language:english'
    elif language == "telugu":
        query += ' language:telugu'
    elif language == "tamil":
        query += ' language:tamil'
    
    results = sp.search(q=query, limit=limit, type='track')
    for track in results['tracks']['items']:
        recommendations.append(track['external_urls']['spotify'])
        
    return recommendations[:limit]

def main():
    st.title("Webcam Emotion Detector")

    # Create a dropdown for selecting language
    language = st.selectbox("Select Language", ["English", "Telugu", "Tamil"])

    # Create a button to capture image from webcam
    if st.button("Capture Image"):
        # OpenCV code to capture image from webcam
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        # Detect emotions
        results = detect_emotion(frame)
        
        # Get the dominant emotion
        dominant_emotion = max(results, key=lambda x: x.get('score', 0)).get('label', 'neutral')

        # Display captured image
        st.image(frame, channels="BGR", caption="Captured Image")

        # Draw emotions on the image
        image_with_emotions = draw_emotions(frame, results)

        # Display image with detected emotions
        st.image(image_with_emotions, channels="BGR", caption=f"Emotions Detected: {dominant_emotion}")

        # Recommend songs based on the dominant emotion and selected language
        recommended_songs = recommend_songs(dominant_emotion, language.lower())
        
        # Display recommended songs
        for i, song_link in enumerate(recommended_songs, start=1):
            st.markdown(f"Song {i}: [Song Link]({song_link})")

if __name__ == "__main__":
    main()