import shutil

src_dockerfile = '../kubernetes-mt/backend/Dockerfile'
src_requirements = '../kubernetes-mt/backend/requirements.txt'
for i in range(10):
    dst_dockerfile = './zona{}/backend/Dockerfile'.format(i)
    dst_requirements = './zona{}/backend/requirements.txt'.format(i)
    shutil.copyfile(src_dockerfile,dst_dockerfile)
    shutil.copyfile(src_requirements,dst_requirements)
    replacement = ["	'host':'mysql-external-service-{}',".format(i) ,"	'database':'rodrigo_docker{}',".format(i),"	'user':'rodrigo_docker{}',".format(i)]
    f_read = open('../kubernetes-mt/backend/api.py','r').readlines()
    f_out = open('./zona{}/backend/api.py'.format(i),'wt')
    
    for j in range(len(f_read)):
        if j == 22:
            f_out.write(replacement[0]+'\n')
        elif j == 24:
            f_out.write(replacement[1]+'\n')
        elif j == 25:
            f_out.write(replacement[2]+'\n')
        else:
            f_out.write(f_read[j])

    f_out.close()