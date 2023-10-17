import streamlit as st
import numpy as np
import pandas as pd
import pickle as pk
import requests

st.title('Movie Recommender System')

movies_list = pk.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_list)

similarity = pk.load(open('similarity.pkl','rb'))


def fetch_posters(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c8c9990ab0527566136149a21107cb42&language=en-US'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/original{poster_path}"
    else:
        return None
    

def fetch_Homepage(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c8c9990ab0527566136149a21107cb42&language=en-US'
    response = requests.get(url)
    data = response.json()
    Homepage = data.get('homepage')
    if Homepage:
        return Homepage
    else:
        return None
    
def fetch_tagline(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c8c9990ab0527566136149a21107cb42&language=en-US'
    response = requests.get(url)
    data = response.json()
    tagline = data.get('tagline')
    if tagline:
        return tagline
    else:
        return None
    



def recommended(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_mov = []
    movie_posters = []
    movie_Homepage = []
    movie_tagline = []
    for i in movies_list:
        recommended_mov.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].id
        poster_url = fetch_posters(movie_id)  # Fetch poster URL using fetch_posters
        poster_homepage = fetch_Homepage(movie_id)
        tagline = fetch_tagline(movie_id)
        if poster_url:
            movie_posters.append(poster_url)

        else:
            movie_posters.append("")

        if poster_homepage:
            movie_Homepage.append(poster_homepage)

        else:
            movie_Homepage.append("")

        
        
        if tagline:
            movie_tagline.append(tagline)
        else:
            movie_tagline.append("")


    # print(movie_tagline)
    return recommended_mov, movie_posters, movie_Homepage, movie_tagline


Selected_movie = st.selectbox(
   "Select your movie?",
   movies['title'],
   index=None,
   placeholder="Select movie...",
)




if st.button("Recommend"):
    Recommended_movies, posters, homepage, tagline = recommended(Selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    for i in range(5):
        col = eval(f"col{i+1}")  # Get the appropriate column object
        with col:
            st.text(Recommended_movies[i])
            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster not available")
            
            if homepage[i]:
                st.write(f"[Homepage]({homepage[i]})")
            else:
                st.write("")

            if tagline[i]:
                st.caption(tagline[i])
            else:
                st.write("")










