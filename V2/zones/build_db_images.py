import os
import time
start_time = time.time()
print('FROM V2 ZONES !!!!!!!!!!')
for i in range(10):
    print('Building rodrigodocker123/mtpreloaded:{} .'.format(i),' docker image')
    os.chdir('./zona{}/preloaded'.format(i))
    os.system('docker build -t rodrigodocker123/mtpreloaded:{} .'.format(i))
    print('Pushing rodrigodocker123/mtpreloaded:{} .'.format(i),' docker image')
    os.system('docker push rodrigodocker123/mtpreloaded:{}'.format(i))
    print('Deleting rodrigodocker123/mtpreloaded:{} .'.format(i),' docker image')
    os.system('docker rmi rodrigodocker123/mtpreloaded:{}'.format(i))
    os.chdir('../../')

print("--- %s seconds ---" % (time.time() - start_time))
