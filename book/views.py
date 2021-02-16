from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from .forms import CommentForm
from django.shortcuts import render, get_object_or_404

# Create your views here.
import pandas as pd
df1=pd.read_csv('recommendation_system/assets/IMDb movies.csv')
df2=pd.read_csv('recommendation_system/assets/book_data.csv')
df1=df1[df1['reviews_from_critics']>50]
df1=df1.sort_values(by=['avg_vote','reviews_from_critics'],ascending=False)
df1.reset_index(drop=True, inplace=True)
df2=df2.drop_duplicates(subset=['book_title'])
df2=df2[df2['book_rating_count']>7500]
df2=df2.sort_values(by=['book_rating'],ascending=False)
df2=df2[:9722]
df1.reset_index(drop=True, inplace=True)
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')

df2['book_desc'] = df2['book_desc'].fillna('')

df1['description'] = df1['description'].fillna('')


tfidf_matrix1 = tfidf.fit_transform(df1['description'])

tfidf_matrix2 = tfidf.transform(df2['book_desc'])

from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix1, tfidf_matrix2)

indices1 = pd.Series(df1.index, index=df1['original_title']).drop_duplicates()

indices2 = pd.Series(df2.index, index=df2['book_title']).drop_duplicates()

    
def get_book(movie):
    def get_recommendations(title, cosine_sim=cosine_sim):
        idx = indices1[title]

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return df2['book_title'].iloc[movie_indices]

    rec = get_recommendations(movie)
    return list(rec)

def recommend_book(request):
    if request.method=='POST':
        books = get_book(movie=request.POST['title'])
        book_list=[]
        global df2
        for i in books:
            df=df2.loc[df2['book_title'] == i]
            recs={}
            recs["title"]=list(df['book_title'])[0]
            recs["desc"] = list(df['book_desc'])[0]
            recs["book_authors"] = list(df['book_authors'])[0]
            recs["genres"] = list(df['genres'])[0]
            recs["image_url"] = list(df["image_url"])[0]
            book_list.append(recs)
        return render(request, 'book_recommendations.html', {'book_list':book_list})
    else:
        return render(request,'get_movie.html')

def about(request):
    return render(request,'about.html')


