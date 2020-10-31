from flask import Flask, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'robin_films'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_CHARSET'] = 'utf-8'
mysql.init_app(app)



@app.route('/films_searched/<str>', methods=['GET'])
def search_films(str):
	sql = '''
		SELECT * FROM robin_films WHERE Title LIKE %?%
					  OR TitleVN LIKE %?%
					  OR Genre LIKE %?%
					  OR Director LIKE %?%
	'''
	cur = mysql.connection.cursor()
	rows = cur.execute(sql, (str,)).fetchall()
	mysql.connection.commit()

	cur.close()

	data=[]
	for r in rows:
		data.append({
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

	return jsonify ({'films: data'})
if __name__ == '__main__':
	app.run()
