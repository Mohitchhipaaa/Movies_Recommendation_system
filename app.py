import streamlit as st
import pickle
import pandas as pd



def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title) 
    return recommended_movies
       
movies_list=pickle.load(open('moviess.pkl','rb'))

movies=pd.DataFrame(movies_list)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title("MOVIES RECOMMANDATION SYSTEM")

select_movie_name=st.selectbox(
    ' How Would you like to be contacted?',
    movies['title'].values
)
if st.button('Recommend'):
    recommentation=recommend(select_movie_name)
    for i in recommentation:
        st.write(i)