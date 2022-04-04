# genera los archivos json de cada zona

import os 
import json
suma = 0
for i in range(10):
    print(i, end = ' ')
    # por cada zona se sacan los estados
    f = open('zona{}/preloaded/zona{}.txt'.format(i,i),'w')
    f1 = open('zona{}/zona{}.json'.format(i,i))
    data = json.load(f1)
    
    STATES = [] # lista de estados o grandes zonas -> representadas por el primer digito del zipcode
    for j in range(len(data)):
        if len(STATES)==0:
            STATES.append(data[j]['fields']['location'].split('-')[2])
        else:
            if data[j]['fields']['location'].split('-')[2] not in STATES:
                STATES.append(data[j]['fields']['location'].split('-')[2])

    # print(i)
    print(STATES)
    #print('     ',len(STATES))
    suma += len(STATES)

    location_per_state = [ [] for i in STATES] # por cada elemento en states crea una lista

    for j in data:
        if j['fields']['location'].split('-')[2] in STATES:
            index = STATES.index(j['fields']['location'].split('-')[2])
            location_per_state[index].append(j['fields']['coord'])
    
    for j in range(len(location_per_state)):
        clat = 0
        clng = 0
        for k in range(len(location_per_state[j])):
            clat += location_per_state[j][k][0]
            clng += location_per_state[j][k][1]
        
        f.write('placeholder,{},{},{},{},{}|\n'.format(STATES[j],str(len(location_per_state[j])),str(round(clat/len(location_per_state[j]),2)),str(round(clng/len(location_per_state[j]),2)),4))
        
    
    count = 0
    
    scf = []
    
    for j in data:
        if len(scf)==0:
            scf.append(j['fields']['zipcode'][1:3])
        else:
            if j['fields']['zipcode'][1:3] not in scf:
                scf.append(j['fields']['zipcode'][1:3])

    location_per_scf = [ [] for i in scf ]

    for j in data:
        if j['fields']['zipcode'][1:3] in scf:
            index = scf.index(j['fields']['zipcode'][1:3])
            location_per_scf[index].append(j['fields']['coord'])

    #print(len(location_per_scf))

    for j in range(len(location_per_scf)):
        clat = 0
        clng = 0
        for k in range(len(location_per_scf[j])):
            clat += location_per_scf[j][k][0]
            clng += location_per_scf[j][k][1]
        f.write('placeholder,{},{},{},{},{}|\n'.format(scf[j],str(len(location_per_scf[j])),str(round(clat/len(location_per_scf[j]),2)),str(round(clng/len(location_per_scf[j]),2)),6))

    cities = []
    for j in data:
        if len(cities) == 0:
            cities.append(j['fields']['location'].split('-')[3])
        else:
            if j['fields']['location'].split('-')[3] not in cities:
                cities.append(j['fields']['location'].split('-')[3])


    location_per_city = [[] for i in cities]
    print(len(location_per_city))
    for j in data:
        if j['fields']['location'].split('-')[3] in cities:
            index = cities.index(j['fields']['location'].split('-')[3])
            if j['fields']['location'].split('-')[3] not in location_per_city[index]:#elimina duplicados
                location_per_city[index].append(j['fields']['coord'])

    for j in range(len(location_per_city)):
        clat = 0
        clng = 0
        for k in range(len(location_per_city[j])):
            clat += location_per_city[j][k][0]
            clng += location_per_city[j][k][1]
        f.write('placeholder,{},{},{},{},{}|\n'.format(cities[j],str(len(location_per_city[j])),str(round(clat/len(location_per_city[j]),2)),str(round(clng/len(location_per_city[j]),2)),8))


print("Cantidad total de estados o zonas grandes : ",suma)