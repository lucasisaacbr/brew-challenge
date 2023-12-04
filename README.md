# Brew Challenge

### What you need to begin ?
- Docker
- Docker-Compose

### What containers it will provide ?
- brew-notebooks: A JupyterHub platform to play with the data. 
- airflow: All containers needed so Airflow can manage the jobs.

### Building the Docker Image

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
service ssh start
```

To facilitate the access grant permissions to $NB_USER and change the password of the user `root`
> Note: This is not recommended in production environments. It's just for the demo purpose.
```
chown -R ${NB_USER} /home/${NB_USER}
passwd
root
root
```
**Why are we doing this ?** 
 - This will give access to user create files in JupyterHub
 - the password is required to connect SSH on airflow, and we don't know the current password for the root user on this image.


To test if the SSH Connection is working, you can run this DAG: 

http://localhost:8080/dags/brew_ssh_test


To activate the `brew_dag` which contains all tasks:

http://localhost:8080/dags/brew_dag

>**PS: It's schedule to run every 15 minutes. Make sure to check if nothing is running  in parallel. 
It may cause conflicts due to I/O operations on disk.**

#### Brew DAG Tasks Description

> --- 
> - **Bronze**: Hit the openbrewerydb API and save the JSONs retured inside the volume `/data/bronze`
> ---
> - **Silver**: Partitions data by Country and State, then save the files as parquets in `/data/silver/brewery_country={}/brewery_state={})`
> ---
> - **Gold**: Read parquets from silver to aggregate the values to return the count of breweries by type and location, prints the results from each country in the screen, and save the files as parquets in `/data/gold/country={}/state={}`
> ---

### Application logs:

#### Bronze

#### Silver

#### Gold 

> If you want to play with the data you can create a notebook in JupyterHub, the token to access it always changes. Check the token in the logs from `docker compose up`
> 