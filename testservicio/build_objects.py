import os
# crea los objetos usando los yaml

os.chdir('./api')
# os.system('kubectl apply -f api.yaml')
# os.system('kubectl apply -f api-external-service1.yaml')
# os.system('kubectl apply -f db1.yaml')
# os.system('kubectl apply -f db-external-service1.yaml')
os.system('kubectl delete -f api.yaml')
os.system('kubectl delete -f api-external-service.yaml')
os.system('kubectl delete -f db1.yaml')
os.system('kubectl delete -f db-external-service1.yaml')
# os.system('ls')
for i in range(2,10): # no se toma la zona 0 porque el dataset repite datos con la zona 1
    os.chdir('../api{}'.format(i))
    # os.system('ls')
    # os.system('kubectl apply -f api{}.yaml'.format(i))
    # os.system('kubectl apply -f api-external-service{}.yaml'.format(i))
    # os.system('kubectl apply -f db{}.yaml'.format(i))
    # os.system('kubectl apply -f db-external-service{}.yaml'.format(i))
    os.system('kubectl delete -f api{}.yaml'.format(i))
    os.system('kubectl delete -f api-external-service{}.yaml'.format(i))
    os.system('kubectl delete -f db{}.yaml'.format(i))
    os.system('kubectl delete -f db-external-service{}.yaml'.format(i))
