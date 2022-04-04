# RodrigoMTV2
MT Project code last version

How to build the app
go to the V2/zones Folder and run the build_backend_images.py and the build_db_images.py, this will create and push the docker images into a docker repository, then run the build_kubernetes_objects.py to deploy everything inside the cluster
after that go to the testservicio folder and create de docker images for the frontend(flask-app-test folder) and the service and you are done.

Description of folders



The folder V2 you will find everything to build the microservices, it has python scripts to separate the dataset in zones, creating backend, the database, the docker images, the yaml files to deploy the app to kubernetes, this scripts are in the zones folder inside the V2 folder,
basically the script uses as a base the code inside the kubernetes-mt folder to create the backend for each microservice and uses the files inside the Preloaded folder to create the databases. 
Then for the service that calculates the k nearest neighbors you must use the code inside the testservicio folder, in this folder you will find folders under the name of api, api2, api3, etc this backends and the zones backend are the same, the code for the service is inside of the folder  called service, inside this folder there are the files to create the docker images, the pod and the service for kubernetes
The frontend is also inside the testservice folder, the folder called flask_app_test contains the necesary files to create a pod with the frontend, the rest was just for testing, currently the flask_app_test for some reason is not working now due an error with the js to create an isntance of the map(google maps script that you must use to have access to a developer map)
