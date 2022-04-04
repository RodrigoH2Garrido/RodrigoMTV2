import os
# crea los objetos usando los yaml

os.chdir('./api')
os.system('docker build -t rodrigodocker123/mtprueba .')
os.system('docker push rodrigodocker123/mtprueba')
os.system('docker rmi rodrigodocker123/mtprueba')

# os.system('ls')
for i in range(2,10): # no se toma la zona 0 porque el dataset repite datos con la zona 1
    os.chdir('../api{}'.format(i))
    # os.system('ls')
    os.system('docker build -t rodrigodocker123/mtprueba:{} .'.format(i))
    os.system('docker push rodrigodocker123/mtprueba:{}'.format(i))
    os.system('docker rmi rodrigodocker123/mtprueba:{}'.format(i))