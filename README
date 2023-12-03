# Brew Challenge

### Building the  Image
This image contains the pyspark-jupyter notebooks. But also some configurations were included to support SSH connections.


Also, in this container contains the python files with APIs and Spark  Jobs.

The Spark Infrastructure resides in this image as well. 

To build run:

$```docker build -t {YOUR_DOCKER_HUB_USERNAME}/pyspark-notebook:latest ./docker```

ps: the last parameter `./docker` should be executed in the root folder of this repo.

### Running Docker Compose

Run the following command to create all the necessary images for the execution.

$`docker-compose up`

check the IPAddress of the brew-notebooks container  (check the `Networks` key from the JSON):

``docker inspect brew-notebooks``

Airflow interface can be accessed on http://localhost:8080

Create a new SSH connection in the panel:

``Admin >> Connection >> + ``

Add the following instructions and hit SAVE: 
```
Connection ID = brew-notebooks
Connection Type = SSH
Description = Connection with brew-noteboks
HOST = The IPAddress from brew-notebooks
USER = root
PASSWORD = root
PORT = 22
```

In the brew-notebooks container make sure that the SSH service is working and setup the root password

```commandline
docker exec -it brew-notebooks bash
# inside the container

service ssh status
service ssh start # if is not running
passwd
root
root
```

To test you can run this DAG:
http://localhost:8080/dags/brew_ssh_test