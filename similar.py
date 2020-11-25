import Personal
from flask import Flask,jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import pandas as pd

app = Flask(__name__)
#api = Api(app)


@app.route('/film/<int:iduser>', methods=['GET'])
def getFilm(iduser):
	user_rate = Personal.getFilm(iduser)
	
	similar_films = pd.DataFrame()
	for film, rate in user_rate:
		similar_films = similar_films.append(Personal.get_similar_movies(film, rate), ignore_index=True)

	similar_films = similar_films.sum().sort_value(ascending=False)
	data = similar_films.keys()
	films = []
	for i in data:
		r = Personalt.get_film_by_id(i)
		films.append({
			'id': r[0],
			'title': r[1],
			'titleVN': r[2],
			'release': r[3],
			'certificate': r[4],
			'runtime': r[5],
			'genre': r[6],
			'rates': r[7],
			'directors': r[8]
			})

	return jsonify ({'similar': films})
#api.add_resource(Film, "/film/<int:iduser>")
if __name__ == '__main__':
	app.run()