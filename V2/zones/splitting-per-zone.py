import json
import requests
import os
# crea las carpetas y los json separados por zonas
print('Before Executing splitting-per-zone.py\n')
os.system('ls')
print('\n')
print('*****'*20)
#crea una carpeta por cada zona del US-MAP-ZIPCODE -> de acuerdo a wikipedia son 9 zonas -> cada zona sera un microservicio
for i in range(10):
    #print(i)
    dir = os.path.join("./","zona"+str(i))  
    if not os.path.exists(dir):
        os.mkdir(dir)
    backend = os.path.join("./","zona"+str(i),"backend")
    if not os.path.exists(backend):
        os.mkdir(backend)
    preloaded = os.path.join("./","zona"+str(i),"preloaded" )
    if not os.path.exists(preloaded):
        os.mkdir(preloaded)
    yaml = os.path.join("./","zona"+str(i),"yaml_files" )
    if not os.path.exists(yaml):
        os.mkdir(yaml)
    backend = os.path.join('./','zona'+str(i))
    if not os.path.exists(backend):
        os.mkdir(backend)
# lectura del dataset

f = open('us-zip-codes.json')
data = json.load(f) 
# print(type(data))
# print(len(data))
# print("----"*40)
zona0 = []
zona1 = []
zona2 = []
zona3 = [] 
zona4 = []
zona5 = []
zona6 = []
zona7 = []
zona8 = []
zona9 = []
for i in range(len(data)):
    if 'coord' in data[i]['fields']: # si el campo coord existe en el data fields pregunta am que zona pertenece y lo agrega a la lista correspondiente.
        if data[i]['fields']['zipcode'][0] == '0':
            zona0.append(data[i])
        elif data[i]['fields']['zipcode'][0] == '1':
            zona1.append(data[i])
        elif data[i]['fields']['zipcode'][0] == '2':
            zona2.append(data[i])
        elif data[i]['fields']['zipcode'][0] == '3':
            zona3.append(data[i])
        elif data[i]['fields']['zipcode'][0] == '4':
            zona4.append(data[i])
        elif data[i]['fields']['zipcode'][0] == '5':
            zona5.append(data[i])
        elif data[i]['fields']['zipcode'][0] == '6':
            zona6.append(data[i])            
        elif data[i]['fields']['zipcode'][0] == '7':
            zona7.append(data[i])
        elif data[i]['fields']['zipcode'][0] == '8':
            zona8.append(data[i])
        elif data[i]['fields']['zipcode'][0] == '9':
            zona9.append(data[i])            


with open('./zona0/zona0.json','w') as linea: 
    json.dump(zona1,linea)

with open('./zona1/zona1.json','w') as linea: 
    json.dump(zona1,linea)

with open('./zona2/zona2.json','w') as linea: 
    json.dump(zona2,linea)

with open('./zona3/zona3.json','w') as linea: 
    json.dump(zona3,linea)

with open('./zona4/zona4.json','w') as linea: 
    json.dump(zona4,linea)

with open('./zona5/zona5.json','w') as linea: 
    json.dump(zona5,linea)

with open('./zona6/zona6.json','w') as linea: 
    json.dump(zona6,linea)

with open('./zona7/zona7.json','w') as linea: 
    json.dump(zona7,linea)

with open('./zona8/zona8.json','w') as linea: 
    json.dump(zona8,linea)

with open('./zona9/zona9.json','w') as linea: 
    json.dump(zona9,linea)

print('\n')
print('After Executing splitting-per-zone.py\n')
os.system('ls')
print('\n\n\n')