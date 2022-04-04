import os
import time
start_time = time.time()
print("DESDE V2 !!!")
for i in range(10):
    os.chdir('./zona{}/backend'.format(i))
    os.system('docker build -t rodrigodocker123/mtbackend2:{} .'.format(i))
    os.system('docker push rodrigodocker123/mtbackend2:{}'.format(i))
    os.system('docker rmi rodrigodocker123/mtbackend2:{}'.format(i))
    os.chdir('../../')
    
print("--- %s seconds ---" % (time.time() - start_time))
