import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "5d3dc30672e74b55a039637921bf7eea"
CLIENT_SECRET = "d08433bbd44f4013a082ae2e0ae92dbd"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_artists = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_music_artists.append(artist)

    return recommended_music_names, recommended_music_artists, recommended_music_posters


# Streamlit app
st.set_page_config(page_title="Music Recommender", page_icon=":notes:", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: black;
        color: #00FF00; /* Bright green text for better contrast */
        font-family: 'Arial', sans-serif;
    }
    .stButton button {
        background-color: #1DB954 !important;
        color: white !important;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;
    }
    .stButton button:hover {
        background-color: white !important;
        color: black !important;
        border: 2px solid #1DB954 !important;
    }
    .stButton button:focus, .stButton button:active {
        background-color: #1DB954 !important;
        color: white !important;
        border: none !important;
    }
    .stSelectbox, .stText, .stImage {
        color: #00FF00; /* Bright green text for better contrast */
    }
    .box {
        border: 2px solid #1DB954;
        border-radius: 12px;
        padding: 10px;
        margin: 10px;
        text-align: center;
        color: #00FF00; /* Bright green text for better contrast */
    }
    .header {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        text-shadow: 2px 2px 5px #000000;
    }
    .subheader {
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 1px 1px 3px #000000;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="header">🎵 Music Recommender System 🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Discover new music based on your favorite songs</div>', unsafe_allow_html=True)

music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list,
    key='selectbox'
)

if st.button('Show Recommendation'):
    with st.spinner('Finding recommendations...'):
        recommended_music_names, recommended_music_artists, recommended_music_posters = recommend(selected_song)

        cols = st.columns(5)
        for col, name, artist, poster in zip(cols, recommended_music_names, recommended_music_artists,
                                             recommended_music_posters):
            with col:
                st.markdown(f"<div class='box'><p>{name} - {artist}</p><img src='{poster}' width='100%'></div>",
                            unsafe_allow_html=True)
