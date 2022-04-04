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

# para local
url_list = []
for i in range(0,9):
	url_list.append('http://192.168.49.2:{}/api/locations'.format(30138+i))

# para cluster eks
#url_list = []
#for i in range(0,9):
#    url_list.append('http://18.118.154.162:{}/api/locations'.format(30138+i))

#url_list = []
# for i in range(1,10):
#     url_list.append('http://api-external-service-test{}/api/locations'.format(i))

# el servicio cuando parte hacer query a todos los getlocations por zoom a todos las apis con los tres niveles de zoom
# entonces guardar por numero de microservicio el nivel de zoom con sus repesctivos punto superior derecho y punto superior izquierdo
# y usar estos valores para saber si se le debe hacer la llamada al microservicio, de esta forma desde el front al mandar el map boundaries
# corroborar cuales son los microservicios que estan dentro y evitar consultar a todos
# entonces cuando se renderizen los puntos por primera vez mandar los puntos y los valores estos para que desde el front se decida

NE_lat = []
SW_lat = []
NE_lng = []
SW_lng = []

boundaries = {} #esto caga cuandos e dockeriza por el las ips de los kubvtl no existen dentro del contianer

for zum in [4,6,8]:
    boundaries[zum] = []
    for j in range(len(url_list)):
        try:
            print('Para url: ',url_list[j]+'/zoom/{}'.format(zum))
            req = requests.get(url_list[j]+'/zoom/{}'.format(zum))
            dataTest = req.json()
            #lista normal
            # for i in dataTest:
            #     print('(',i['lat'],',',i['lng'],')  ---> ',math.sqrt(float(i['lat'])**2+float(i['lng'])**2))

            #lista ordenada por lng de menor a mayor
            dataTest.sort(  key = lambda element: float(element['lng'])) 
            NE_lng = dataTest[-1]['lng']
            SW_lng = dataTest[0]['lng']

            #lista ordenada por lat de menor a mayor
            dataTest.sort(  key = lambda element: float(element['lat'])) 
            NE_lat = dataTest[-1]['lat']
            SW_lat = dataTest[0]['lat']
            # print('NE = ({},{})'.format(NE_lat[-1],NE_lng[-1]))
            # print('SW = ({},{})'.format(SW_lat[-1],SW_lng[-1]))
            # print(type(SW_lng[-1]))
            # print("*"*20)
            boundaries[zum].append({
                'fromlat':float(SW_lat),
                'tolat':float(NE_lat),
                'fromlng':float(SW_lng),
                'tolng':float(NE_lng)
            })
        except requests.exceptions.RequestException as e:
                    print('entro falla acá')
                    print(e)
   

print(boundaries)
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
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyAzx3SkOkxsSTdfvApBWit0q19xVeISFZ0'.format(address) 
    r = requests.get(url)
    data = r.json()
    #sdprint("DATA: ",data)
    address_obj = {
        'lat': data['results'][0]['geometry']['location']['lat'],
        'lng':data['results'][0]['geometry']['location']['lng'],
        'place':address
    }

    ms_data = {
        'location':address_obj,
        'k':k
    }

    for url in url_list:
        try:
            r2 = requests.get(url+'/knearest/{}/{}/{}/{}/{}'.format(zoom,fromlat,tolat,fromlng,tolng),json=ms_data)
            data2 = r2.json()
            #print('aksjds')
            ms_k_neighbors = ms_k_neighbors + data2 # se van añadiendo los puntos retornados por los microservicios
        except requests.exceptions.RequestException as e:
            print(e)

    ms_final_neighbors = closestPoints(ms_k_neighbors,k,address_obj)
    ms_final_neighbors.append(address_obj)
    print(ms_final_neighbors)
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
                #print(len(data))
            except requests.exceptions.RequestException as e:
                print(e)    
        location_data = datitos
        auxVar = 123
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
        #print(len(datitos))
        return jsonify(datitos)
    return "not working 2"



@app.route('/service/getLocations/zoom3/<int:zoom>/<string:fromlat>/<string:tolat>/<string:fromlng>/<string:tolng>',methods=['GET','POST'])
def getLocationsInBounds2(zoom,fromlat,tolat,fromlng,tolng):
    if request.method == 'GET':
        datitos=[]
        print(type(zoom))
        print(zoom)
        print('len datitos ',len(datitos))
        if zoom < 6:
            boundaries_list = boundaries[4]
            zum = 4
        elif zoom >= 6 and zoom < 8:
            boundaries_list = boundaries[6]
            zum = 6
        elif zoom >= 8:
            boundaries_list = boundaries[8]
            zum = 8
        for i in  range(len(url_list)):
            if boundaries_list[i]['fromlng'] < float(tolng) and\
                boundaries_list[i]['fromlat'] < float(tolat) and\
                boundaries_list[i]['tolat'] > float(fromlat) and\
                boundaries_list[i]['tolng'] > float(fromlng):
                print("Caso 4.1 ms: ",i)
                try:
                    req = requests.get(url_list[i]+'/zoom2/{}/{}/{}/{}/{}'.format(zum,fromlat,tolat,fromlng,tolng))
                    data = req.json()
                    datitos += data
                except requests.exceptions.RequestException as e:
                    print(e)
            else:
                print('ms: ',i,'\n',boundaries_list[i])
                print('**'*20)
        print('len datitos ',len(datitos))
        return jsonify(datitos)
    return "not working 3"




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
    app.run(host='0.0.0.0',port=5000)
