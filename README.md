Install the dependencies

pip install -r requirements.txt

1. Fill in the Spotify credentials:

Before running the application, make sure to fill in your Spotify API credentials in the code:

```python
# Spotify credentials
SPOTIFY_CLIENT_ID = 'your_client_id'
SPOTIFY_CLIENT_SECRET = 'your_client_secret'

Replace 'your_client_id' and 'your_client_secret' with your actual Spotify API credentials.

Run the Streamlit application:

python -m streamlit run main.py