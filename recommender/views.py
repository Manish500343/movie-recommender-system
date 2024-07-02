from django.shortcuts import render
import pandas as pd
import pickle
import requests
import gdown

def fetch_poster(movie_id):
    headers = {"accept": "application/json"}
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=ab4aa40d8f8bbba3d919ad29130e8319&language=en-US".format(movie_id), headers=headers)
    data = response.json()
    poster_path = data.get("poster_path")
    base_url = "https://image.tmdb.org/t/p/w500"
    full_poster_url = f"{base_url}{poster_path}"
    return full_poster_url

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

with open('recommender/movie_dict.pkl', 'rb') as file:
    movie_dict = pickle.load(file)

movies = pd.DataFrame(movie_dict)

file_id = '1Jldsn13Hw8QCO18HBh8mWQjGlmZL4H94'
destination = 'similarity.pkl'
url = f'https://drive.google.com/uc?export=download&id={file_id}'
gdown.download(url, destination, quiet=False)

with open(destination, 'rb') as file:
    similarity = pickle.load(file)

def home(request):
    return render(request, 'main.html', {'movies': movies['title']})

def recommendation_view(request):
    if request.method == 'POST':
        selected_movie = request.POST.get('selected_movie')
        recommended_movies, recommended_posters = recommend(selected_movie)
        recommendations = zip(recommended_movies, recommended_posters)
        return render(request, 'main.html', {'movies': movies['title'], 'recommendations': recommendations})
    return render(request, 'main.html', {'movies': movies['title']})

with open('recommender/detail.pkl', 'rb') as file:
    all_detail = pickle.load(file)

def movie_detail(request, movie_title):
    one_detail = all_detail[all_detail.title == movie_title].to_dict(orient='records')[0]
    return render(request, 'movie_detail.html',{'one_detail': one_detail})


    
