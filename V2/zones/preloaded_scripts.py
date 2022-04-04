import shutil
import os
#este script copia los archivos del preloaded original y cambia las contrasenas y nombres de las tablas

src_install = '../Preloaded/install_mysql.sh'
src_dockerfile = '../Preloaded/Dockerfile'

for i in range(10):
    dst_install = './zona{}/preloaded/install_mysql.sh'.format(i)
    dst_dockerfile = './zona{}/preloaded/Dockerfile'.format(i)
    shutil.copyfile(src_install,dst_install)
    shutil.copyfile(src_dockerfile,dst_dockerfile)
    replace = ["usertest='rodrigo_docker{}'".format(i),"LOAD DATA LOCAL INFILE 'zona{}.txt' INTO TABLE locations CHARACTER SET utf8 FIELDS TERMINATED BY".format(i) + " ',' "+ "LINES TERMINATED BY '|' ;".format(i)]
    
    f_load = open('../Preloaded/load_data.sh','r').readlines()
    fout_load = open('./zona{}/preloaded/load_data.sh'.format(i),'wt')

    for j in range(len(f_load)):
        if j == 4:
            fout_load.write(replace[0]+'\n')
        elif j == 40:
            fout_load.write(replace[1]+'\n')
        else:
            fout_load.write(f_load[j])

    fout_load.close()

    f_select = open('../Preloaded/select_data.sh').readlines()
    fout_select = open('./zona{}/preloaded/select_data.sh'.format(i),'wt')

    for i in range(len(f_select)):
        if i == 5:
            fout_select.write(replace[0]+'\n')
        else:
            fout_select.write(f_select[i])

    fout_select.close()