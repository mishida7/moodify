from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS  # Import CORS
app = Flask(__name__)
CORS(app)
# Define the Gemini API endpoint and your API key (replace with your actual key)
GEMINI_API_URL = "https://api.gemini.com/v1/music/suggestions"
GEMINI_API_KEY = "YOUR_API_KEY"

# Map emojis to moods
emoji_to_mood = {
    "😀": "happy",
    "😢": "sad",
    "😎": "cool",
    "😠": "angry",
    "😌": "relaxed",
    "🥳": "excited",
    # Add more emojis and moods as needed
}

# Function to get song suggestions from Gemini API based on mood
def get_song_suggestions(mood):
    try:
        response = requests.get(GEMINI_API_URL, params={"mood": mood, "api_key": GEMINI_API_KEY})
        response.raise_for_status()  # Check for request errors
        songs = response.json()  # Assuming Gemini API returns a JSON list of songs
        return songs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Gemini API: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_songs', methods=['POST', 'OPTIONS'])
def get_songs():
    emoji = request.json.get('emoji')
    mood = emoji_to_mood.get(emoji, "neutral")  # Default to neutral if emoji not found
    
    # Fetch song suggestions based on the mapped mood
    songs = get_song_suggestions(mood)
    
    # Return the song suggestions as JSON
    return jsonify(songs)


if __name__ == '__main__':
    app.run(debug=True)
