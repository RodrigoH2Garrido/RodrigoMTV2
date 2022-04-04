import json
from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import sys
import socket

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


#config = {
#        'user': 'rodrigo_docker1',
#        'password': 'Password123#@!',
#        'host': '127.0.0.1',
#        'port': '3307',
#        'database': 'rodrigo_docker1'
        #'ssl_ca': '/rds-combined-ca-bundle.pem'       
#}

# esta config permite conectarse a la base de datos dentro del cluster -> puede que la ip cambie -> es la misma ip del minikube
config = {
	'host':'mysql-external-service-1',
	'port':'3307',
	'database':'rodrigo_docker1',
	'user':'rodrigo_docker1',
	'password':'Password123#@!'  
}

@app.route('/test')
def prueba():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	print(s.getsockname()[0])
	return 'esto es una prueba:'+ str(s.getsockname()[0])
	s.close()

@app.route('/')
def home():
	connection = mysql.connector.connect(**config)
	print('Connection : ',connection,file=sys.stderr)
	connection.close()
	return "working !!!"
	
@app.route('/api/locations',methods=['GET','POST'])
def read_locations():
    if request.method=='GET':
    	connection = mysql.connector.connect(**config)
    	cursor = connection.cursor()
    	select_query='SELECT * FROM locations'
    	cursor.execute(select_query)
    	res = [x for x in cursor]
    	headers = [x[0] for x in cursor.description]
    	cursor.close()
    	connection.close()
    	"""print("."*20,file=sys.stderr)
    	print(res,file=sys.stderr)
    	print("",file=sys.stderr)
    	print(headers,file=sys.stderr)
    	print("."*20,file=sys.stderr)"""    	
    	location_json=[]
    	for i in res:
    		location_json.append(dict(zip(headers,i)))
    	#print(jsonify(location_json).data)
    	return jsonify(location_json)
    return "locations not working!!"

#esta ruta se debera llamar por cada locación que se necesita guardar
@app.route('/api/insert/<string:place>/<int:points>/<string:lat>/<string:lng>/<int:zoom>',methods=['POST'])
def insert(place,points,lat,lng,zoom):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    insert_query = '''INSERT INTO locations (place,points,lat,lng,zoom) values ("{}","{}","{}","{}","{}")'''.format(place,points,lat,lng,zoom)
    cursor.execute(insert_query)
    connection.commit()
    cursor.close()
    connection.close()
    return "work"

# get all the points in a particular zoom level
@app.route('/api/locations/zoom/<int:zoom>',methods=['GET','POST'])    
def getlocationsperzoom(zoom):
	if request.method == 'GET':
		connection = mysql.connector.connect(**config)
		cursor = connection.cursor()
		select_query='SELECT * FROM locations where zoom = {}'.format(zoom)
		cursor.execute(select_query)
		res = [x for x in cursor]
		headers = [x[0] for x in cursor.description]
		cursor.close()
		connection.close()
		location_json=[]
		for i in res:
			location_json.append(dict(zip(headers,i)))
		return jsonify(location_json)
	return "get locations per zoom not working !!!"    

#get all the points in a particular zoom level that are inside of the map view boundaries.

# this solution has the problem that every time the map is dragged or zoomed in or out the app query the points, 

# Lo que se me ocurre es que la primera vez que se obtienen puntos(Cuando el mapa updatea la prmera vez) guardar un registro de esstos puntos(en una tabla
# de la base de datos o en una lista temporal) de esta forma cada vez que se interactua con el mapa se revisan los puntos que ya estan siendo mostrados y se consultan
# solo por los que faltan y se quitan los que no deben ser mostrados, para hacer la consulta solo cuando corresponda

@app.route('/api/locations/zoom2/<int:zoom>/<string:fromlat>/<string:tolat>/<string:fromlng>/<string:tolng>',methods=['GET','POST'])
def getlocationsperBounds(zoom,fromlat,tolat,fromlng,tolng):
	if request.method == 'GET':
		connection = mysql.connector.connect(**config)
		cursor = connection.cursor()
		if zoom < 6:
			select_query = 'SELECT * FROM locations WHERE zoom = 4 AND lat >= {} AND lat <= {} AND lng >= {} AND lng <= {}'.format(fromlat,tolat,fromlng,tolng)
		elif zoom >= 6 and zoom < 8:
			select_query = 'SELECT * FROM locations WHERE zoom = 6 AND lat >= {} AND lat <= {} AND lng >= {} AND lng <= {}'.format(fromlat,tolat,fromlng,tolng)
		elif zoom >= 8:
			select_query = 'SELECT * FROM locations WHERE zoom = 8 AND lat >= {} AND lat <= {} AND lng >= {} AND lng <= {}'.format(fromlat,tolat,fromlng,tolng)			
		cursor.execute(select_query)
		res = [x for x in cursor]
		headers = [x[0] for x in cursor.description] #saca los nombres de las columnas de la tabla locations
		cursor.close()
		connection.close()
		location_json = []
		for i in res:
			location_json.append(dict(zip(headers,i)))
		return jsonify(location_json)
	return "Get Locations Per Zoom and Boundaries is not Working !!! D:"

import math

def closestPoints(lista,k,o):
    lista.sort(  key = lambda element: math.sqrt( (( (o['lat'])-float(element['lat']))**2) +  ((o['lng']-float(element['lng']))**2) )   ) 
    return lista[:k]


@app.route('/api/locations/knearest/<int:zoom>/<string:fromlat>/<string:tolat>/<string:fromlng>/<string:tolng>',methods=['GET','POST'])
def getKnearest(zoom,fromlat,tolat,fromlng,tolng):
	data = request.get_json(force=True)
	k = data['k']
	address_obj=data['location']
	if request.method == 'GET':
		connection = mysql.connector.connect(**config)
		cursor = connection.cursor()
		if zoom < 6:
			select_query = 'SELECT * FROM locations WHERE zoom = 4 AND lat >= {} AND lat <= {} AND lng >= {} AND lng <= {}'.format(fromlat,tolat,fromlng,tolng)
		elif zoom >= 6 and zoom < 8:
			select_query = 'SELECT * FROM locations WHERE zoom = 6 AND lat >= {} AND lat <= {} AND lng >= {} AND lng <= {}'.format(fromlat,tolat,fromlng,tolng)
		elif zoom >= 8:
			select_query = 'SELECT * FROM locations WHERE zoom = 8 AND lat >= {} AND lat <= {} AND lng >= {} AND lng <= {}'.format(fromlat,tolat,fromlng,tolng)			
		cursor.execute(select_query)
		res = [x for x in cursor]
		headers = [x[0] for x in cursor.description] #saca los nombres de las columnas de la tabla locations
		cursor.close()
		connection.close()
		location_json = []
		for i in res:
			location_json.append(dict(zip(headers,i)))

		k_nearest=closestPoints(location_json,k,address_obj)
		print('\n',k_nearest,'\n')
		return jsonify(k_nearest)
	
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
