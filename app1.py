import pickle
import pandas as pd
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from database import create_db
from auth import login_page, signup_page


create_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
st.set_page_config(page_title="Movie Recommender", layout="wide")

if not st.session_state.logged_in:
    st.title("🎬 Movie Recommender System")

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login_page()
    else:
        signup_page()

    st.stop()   

st.sidebar.success(f"Welcome {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()


session = requests.Session()
retries = Retry(total=5, backoff_factor=1)
session.mount('https://', HTTPAdapter(max_retries=retries))

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=040ccb878d300fc22929c4c35b46a11a&language=en-US"
        data = session.get(url).json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    names, posters = [], []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters

movies = pd.DataFrame(pickle.load(open('movie_dct.pkl', 'rb')))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("🍿 Movie Recommender System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

    cols = st.columns(5)
    for i in range(5, 10):
        with cols[i - 5]:
            st.text(names[i])
            st.image(posters[i])
