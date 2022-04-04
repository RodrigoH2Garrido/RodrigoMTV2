FROM ubuntu:18.04
COPY . /home/diicc/mydockerbuild
WORKDIR /home/diicc/mydockerbuild
RUN apt-get update -y
RUN apt-get install --assume-yes apt-utils
RUN apt-get -y install vim
RUN chmod a+x ./install_mysql.sh ./load_data.sh ./select_data.sh
RUN ./install_mysql.sh
RUN ./load_data.sh
RUN rm -f ./install_mysql.sh ./load_data.sh ./0,2M.txt
CMD ./select_data.sh
