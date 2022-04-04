import shutil

#falta lo de la api -> api{}.yaml & api_svc{}.yaml

for i in range(10):
    db_yaml_replacement = ['  name: mysql-ubuntu-deployment-{}'.format(i),'    app: mysql-ubuntu-d-{}'.format(i),'      app: mysql-ubuntu-{}'.format(i),'        app: mysql-ubuntu-{}'.format(i),'        - name: mysql-ubuntu-container{}'.format(i),'          image: rodrigodocker123/mtpreloaded:{}'.format(i)]
    db_svc_yaml_replacement = ['  name: mysql-external-service-{}'.format(i),'    app:  mysql-ubuntu-{}'.format(i),'     nodePort: '+str(30036+i)]
    api_yaml_replacement = ['  name: api-deployment-{}'.format(i),'    app: api-d-{}'.format(i),'      app: api-{}'.format(i),'        app: api-{}'.format(i),'        - name: api-container{}'.format(i),'          image: rodrigodocker123/mtbackend:{}'.format(i)]
    api_svc_yaml_replacement = ['  name: api-external-service-{}'.format(i),'    app:  api-{}'.format(i),'     nodePort: '+str(30137+i)]
    #print(str(30036+i))
    f_db = open('../kubernetes-mt/db.yaml','r').readlines()
    fout_db = open('./zona{}/yaml_files/db{}.yaml'.format(i,i),'wt')

    for j in range(len(f_db)):
        if j == 3:
            fout_db.write(db_yaml_replacement[0]+'\n')
        elif j == 5:
            fout_db.write(db_yaml_replacement[1]+'\n')
        elif j == 10:
            fout_db.write(db_yaml_replacement[2]+'\n')
        elif j == 14:
            fout_db.write(db_yaml_replacement[3]+'\n')            
        elif j == 17:
            fout_db.write(db_yaml_replacement[4]+'\n')
        elif j == 18:
            fout_db.write(db_yaml_replacement[5]+'\n')
        else:
            fout_db.write(f_db[j])
    fout_db.close()

    f_db_svc = open('../kubernetes-mt/db-external-service.yaml','r').readlines()
    fout_db_svc = open('./zona{}/yaml_files/db-external-service{}.yaml'.format(i,i),'wt')
    for j in range(len(f_db_svc)):
        if j == 3:
            fout_db_svc.write(db_svc_yaml_replacement[0]+'\n')
        elif j == 7:
            fout_db_svc.write(db_svc_yaml_replacement[1]+'\n')
        elif j == 12:
            fout_db_svc.write(db_svc_yaml_replacement[2]+'\n')
        else:
            fout_db_svc.write(f_db_svc[j])
    fout_db_svc.close()

    f_api = open('../kubernetes-mt/api.yaml','r').readlines()
    f_api_out = open('./zona{}/yaml_files/api{}.yaml'.format(i,i),'wt')
    for j in range(len(f_api)):
        if j == 3:
            f_api_out.write(api_yaml_replacement[0]+'\n')
        elif j == 5:
            f_api_out.write(api_yaml_replacement[1]+'\n')
        elif j == 10:
            f_api_out.write(api_yaml_replacement[2]+'\n')
        elif j == 14:
            f_api_out.write(api_yaml_replacement[3]+'\n')
        elif j == 17:
            f_api_out.write(api_yaml_replacement[4]+'\n')
        elif j == 18:
            f_api_out.write(api_yaml_replacement[5]+'\n')
        else:
            f_api_out.write(f_api[j])
    f_api_out.close()

    f_api_svc = open('../kubernetes-mt/api-external-service.yaml','r').readlines()
    f_api_svc_out = open('./zona{}/yaml_files/api-external-service{}.yaml'.format(i,i),'wt')

    for j in range(len(f_api_svc)):
        if j == 3:
            f_api_svc_out.write(api_svc_yaml_replacement[0]+'\n')
        elif j == 7:
            f_api_svc_out.write(api_svc_yaml_replacement[1]+'\n')
        elif j == 12:
            f_api_svc_out.write(api_svc_yaml_replacement[2]+'\n')
        else:
            f_api_svc_out.write(f_api_svc[j])
    f_api_svc_out.close()    