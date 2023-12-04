# Brew Challenge

### Building the  Image

This image contains the pyspark-jupyter notebooks. But also some configurations were included to support SSH connections.
Also, this container contains the Python files with APIs and Spark  Jobs.
The Spark Infrastructure resides in this image as well. 

To build run:

```docker build -t {YOUR_DOCKER_HUB_USERNAME}/pyspark-notebook:latest .```

### Running Docker Compose

Run the following command to create all the necessary images for the execution.

`docker-compose up`

### Configuring the environment

1. Check the IPAddress of the brew-notebooks container, by running:

``docker inspect brew-notebooks``

> check the `Networks` key from the JSON to find the IPAddress

Once you get the `IPAddress` we need to configure the Airflow Connection inside  the Dashboard:

Airflow interface can be accessed at http://localhost:8080

>Create a new SSH connection in the panel:
>
>``Admin >> Connection >> + ``
>
>Add the following instructions and hit SAVE: 
>```
>Connection ID = brew-notebooks
>Connection Type = SSH
>Description = Connection with brew-noteboks
>HOST = The IPAddress from brew-notebooks
>USER = root
>PASSWORD = root
>PORT = 22
>```

In the `brew-notebooks` container, make sure that the SSH service is working and setup the root password

Access the container bash  terminal:
```commandline 
docker exec -it brew-notebooks bash
```

In the bash terminal enable the ssh server
```commandline
service ssh status
service ssh start # if is not running
```

To facilitate the access change the password of the user `root`
> Note: This is not recommended in production environments. It's just for the demo purpose.
```
passwd
root
root
```



To test, you can run this DAG:
http://localhost:8080/dags/brew_ssh_test
