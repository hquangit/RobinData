import pandas as pd
from scipy.sparse import csr_matrix 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import sqlite3

data = pd.read_csv("movies_users.csv")
data = data.T

database = 'data/films.db'

def getFilm(iduser):
	conn = sqlite3.connect(database)
	sql1='''
		SELECT film, rate FROM watched_film wf WHERE wf.user=?
	'''
	user_rate = conn.execute(sql1,(iduser,)).fetchall()
	conn.close()
	return user_rate

def get_film_by_id(idfilm):
	conn = sqlite3.connect(database)
	sql1='''
		SELECT * FROM films f WHERE f.id=?
	'''
	film = conn.execute(sql1,(idfilm,)).fetchone()
	conn.close()
	return film

def standardize(row):
	new_row = (row-row.mean())/(row.max() - row.min())
	return new_row

def similarity_data():
	new_data = data.apply(standardize)
	similarity = cosine_similarity(new_data.T)
	similarity_df = pd.DataFrame(similarity, index=data.columns, columns=data.columns)

	return similarity_df

def get_similar_movies(id_movie, user_rating):
	df = similarity_data()
	similar_data = df[id_movie]*(user_rating-2.5)
	similar_data = similar_data.sort_values(ascending=False)
	#similar_data = list(similar_data)
	#data = similar_data.keys()
	#films = []
	#for i in data:
	#	films.append(get_film_by_id(i))
	return similar_data 

if __name__ == '__main__':
	d = [(10,3), (183,4)]
	similar_films=pd.DataFrame()
	for film, rate in d:
		similar_films = similar_films.append(get_similar_movies(film, rate), ignore_index=True)


	similar_films = similar_films.sum().sort_value(ascending=False)
	print(similar_films)