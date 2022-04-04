from os import close
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from flask_restful import  reqparse
from requests.exceptions import RequestException
import math

parser = reqparse.RequestParser()
parser.add_argument('address')
parser.add_argument('neighbors')
parser.add_argument('fromlat')
parser.add_argument('tolat')
parser.add_argument('fromlng')
parser.add_argument('tolng')
parser.add_argument('zoom')

app = Flask(__name__)

cors = CORS(app, resources={ r"/service/*": {"origins": "*"}, r"/api/locations*": {"origins": "*"} })

#url_list = ['http://192.168.43.169:5002/api/locations','http://192.168.43.169:5003/api/locations','http://192.168.43.169:5004/api/locations']
url_list = []
for i in range(0,9):
    url_list.append('http://192.168.49.2:{}/api/locations'.format(30138+i))


def closestPoints(lista,k,o):
    lista.sort(  key = lambda element: math.sqrt( ((o['lat']-float(element['lat']))**2) +  ((o['lng']-float(element['lng']))**2) )   ) 
    return lista[:k]

@app.route('/service/test')
def test():
    return "working"

@app.route('/service/address1',methods=['GET','POST'])
def service():
    ms_k_neighbors=[] # lista que guarda los k vecinos de todos los ms 
    args = parser.parse_args()
    address = args['address']
    fromlat = args['fromlat']
    tolat = args['tolat']
    fromlng = args['fromlng']
    tolng = args['tolng']
    zoom = args['zoom']
    k = int(args['neighbors'])
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key=API_KEY'.format(address) 
    r = requests.get(url)
    data = r.json()
    address_obj = {
        'lat': data['results'][0]['geometry']['location']['lat'],
        'lng':data['results'][0]['geometry']['location']['lng'],
        'place':address
    }

    ms_data = {
        'location':address_obj,
        'k':k
    }

    print("\n",ms_data,'\n')


    try:
        r2 = requests.get('http://192.168.49.2:30138/api/locations/knearest/{}/{}/{}/{}/{}'.format(zoom,fromlat,tolat,fromlng,tolng),json=ms_data)
        data2 = r2.json()
        ms_k_neighbors = ms_k_neighbors+data2
    except requests.exceptions.RequestException as e:
        print(e)
    # for url in url_list:
    #     try:
    #         r2 = requests.get(url+'/knearest/{}/{}/{}/{}/{}'.format(zoom,fromlat,tolat,fromlng,tolng),json=ms_data)
    #         data2 = r2.json()

    #         ms_k_neighbors = ms_k_neighbors + data2 # se van añadiendo los puntos retornados por los microservicios
    #     except requests.exceptions.RequestException as e:
    #         print(e)

    ms_final_neighbors = closestPoints(ms_k_neighbors,k,address_obj)
    ms_final_neighbors.append(address_obj)
    return jsonify(ms_final_neighbors)

@app.route('/service/getLocations',methods=['GET','POST'])
def getLocations():
    if request.method == 'GET':    
        datitos=[]
        for url in url_list:
            try: # permite intentar la conexion y en caso de que algun servicio esté abajo no se cae este servicio
                r = requests.get(url+'/zoom/4')
                data = r.json()
                #print('i: ',i, 'data type: ',type(data), ' url : ',url+'/zoom/4')
                #datitos.append(data)
                datitos += data
            except requests.exceptions.RequestException as e:
                print(e)    
        location_data = datitos
        return jsonify(location_data)




@app.route('/service/getLocations/zoom2/<int:zoom>/<string:fromlat>/<string:tolat>/<string:fromlng>/<string:tolng>',methods=['GET','POST'])
def getLocationsInBounds(zoom,fromlat,tolat,fromlng,tolng):
    if request.method == 'GET':
        datitos=[]
        for url in url_list:
            try:
                r = requests.get(url+'/zoom2/{}/{}/{}/{}/{}'.format(zoom,fromlat,tolat,fromlng,tolng))
                #print(url+'/zoom2/{}/{}/{}/{}/{}'.format(zoom,fromlat,tolat,fromlng,tolng))
                data = r.json()
                datitos += data
            except requests.exceptions.RequestException as e:
                print(e)
        return jsonify(datitos)
    return "not working 2"


@app.route('/service/pokemon',methods=['POST','GET'])
def pokemon(): # replicar esto con todas las url de todos los microservicios y obtener todos los puntos, luego ver como mejorar la logica queriar solo los microservicios que corresponden
    #y ver como hacer esto más rapido, es decir, aplicar el cluster tomando los puntos mas n piuntos mas cercanos al address dado
    datito = []
    pokemons = ['ditto','bulbasaur','ivysaur','charmander','charmeleon','charizard']
    for poke in pokemons:
        url= 'https://pokeapi.co/api/v2/pokemon/{}'.format(poke)
        #r = requests('https://pokeapi.co/api/v2/pokemon/{}'.format(poke))
        #data = r.json()
        r = requests.get(url)
        data = r.json()
        datito.append(data['species'])
    return json.dumps(datito)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)
