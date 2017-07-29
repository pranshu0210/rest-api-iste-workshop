from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
from flask_cors import CORS

import http.client

app = Flask(__name__)
CORS(app)
api = Api(app)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql'
app.config['MYSQL_DATABASE_DB'] = 'heroesdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
connection = mysql.connect()

cursor = connection.cursor()


class Hero(Resource):
	def post(self):	
		try:
			print(request.get_json())
			dataVariable = request.get_json()
		except http.client.HTTPException as e:
			return {"message": "error message"}, 400

		i = cursor.execute("INSERT INTO heroes (Name, Details) VALUES(%s, %s)", (dataVariable["name"], dataVariable["detail"]))
		if i == 0:
			connection.rollback()
			return {"message": "Id not found"}
		connection.commit()
		return { "message": "Success"}
		
	def get(self):
		cursor.execute("SELECT * FROM heroes;")
		info = cursor.fetchall()
		heroes = []
		for i in range(0, len(info)):
			heroes.append({
				"id": info[i][0],
				"name": info[i][1],
				"detail": info[i][2]		
			})
		return jsonify(heroes)
	def put(self):
		try:
			data = request.get_json()
		except http.client.HTTPException as e:
			return {"message": "error message"}, 400
		
		i = cursor.execute("UPDATE heroes SET Name = %s, Details = %s WHERE Id=%s", (data["name"], data["detail"], data["id"]))
		if i == 0:
			connection.rollback()
			return {"message": "Id not found"}
		connection.commit()
		return { "message": "Success"}
		
	def delete(self):
		try:
			data = request.get_json()
		except http.client.HTTPException as e:
			return {"message": "error message"}, 400

		i = cursor.execute("DELETE FROM heroes WHERE Id=%s", data["id"])
		if i == 0:
			connection.rollback()
			return {"message": "Id not found"}
		connection.commit()
		return { "message": "Success" }
		
api.add_resource(Hero, '/hero')

if __name__ == '__main__':
    app.run(debug=False, host='192.168.0.100', port=5000)
