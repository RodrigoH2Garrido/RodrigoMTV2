import os
# crea los objetos usando los yaml
# for i in range(1,10): # no se toma la zona 0 porque el dataset repite datos con la zona 1
#     os.chdir('./zona{}/yaml_files'.format(i))
#     os.system('kubectl apply -f db{}.yaml'.format(i))
#     os.system('kubectl apply -f db-external-service{}.yaml'.format(i))
#     os.system('kubectl apply -f api{}.yaml'.format(i))
#     os.system('kubectl apply -f api-external-service{}.yaml'.format(i))
#     os.chdir('../../')

#borra los objectos

for i in range(1,10):
    os.chdir('./zona{}/yaml_files'.format(i))
    # os.system('kubectl delete -f db{}.yaml'.format(i))
    # os.system('kubectl delete -f db-external-service{}.yaml'.format(i))
    os.system('kubectl delete -f api{}.yaml'.format(i))
    os.system('kubectl delete -f api-external-service{}.yaml'.format(i))
    os.chdir('../../')




#os.system('kubectl get all -o wide')