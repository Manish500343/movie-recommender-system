import pandas as pd
import streamlit as st
import pickle
import requests
import gdown

def fetch_poster(movie_id):
    headers = {"accept": "application/json"}
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=ab4aa40d8f8bbba3d919ad29130e8319&language=en-US".format(movie_id), headers=headers)

    # Parse the JSON response
    data = response.json()

    # Extract the poster path
    poster_path = data.get("poster_path")

    # Construct the full URL for the poster
    base_url = "https://image.tmdb.org/t/p/w500"  # You can use other sizes as well
    full_poster_url = f"{base_url}{poster_path}"

    return (full_poster_url)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True,
                        key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)

# Define the Google Drive file ID and the destination filename
file_id = '1Jldsn13Hw8QCO18HBh8mWQjGlmZL4H94'
destination = 'similarity.pkl'

# Construct the Google Drive URL
url = f'https://drive.google.com/uc?export=download&id={file_id}'

# Use gdown to download the file
gdown.download(url, destination, quiet=False)

# Now load the pickle file
with open(destination, 'rb') as file:
    similarity = pickle.load(file)



st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)

if st.button('Recommend'):
    names,poster=recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
