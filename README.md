# Brew Challenge

### What do you need to begin?
- Docker
- Docker-Compose

### What containers will it provide?
- brew-notebooks: A JupyterHub platform to play with the data. 
- airflow: All containers are needed so Airflow can manage the jobs.

### Building the Docker Image

This image contains the pyspark-jupyter notebooks. Some configurations were also included to support SSH connections.
Also, this container contains the Python files with APIs and Spark  Jobs.
The Spark Infrastructure resides in this image as well. 

To build run:

```docker build -t {YOUR_DOCKER_HUB_USERNAME}/pyspark-notebook:latest .```

> Important! > On `docker-compoer.yml` please change the image name at line 90 to your new image name created in the last step.

### Running Docker Compose

Run the following command to create all the necessary images for the execution.

`docker-compose up`

### Configuring the environment

1. Check the IPAddress of the brew-notebooks container by running:

``docker inspect brew-notebooks``

> Check the `Networks` key from the JSON to find the IPAddress

![image](https://github.com/lucasisaacbr/brew-challenge/assets/22127369/c7982e32-1c1b-40eb-9398-a7097ed437c6)


Once you get the `IPAddress` we need to configure the Airflow Connection inside  the Dashboard:

The airflow interface can be accessed at http://localhost:8080

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

In the `brew-notebooks` container, make sure that the SSH service is working and setup the root password.

Access the container bash  terminal:
```commandline 
docker exec -it brew-notebooks bash
```

In the bash terminal, enable the ssh server
```commandline
service ssh start
```

To facilitate the access, grant permissions to $NB_USER and change the password of the user `root`
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


To activate the `brew_dag`, which contains all tasks:

http://localhost:8080/dags/brew_dag

>**PS: It's scheduled to run every 15 minutes. Make sure to check if nothing is running  in parallel. 
It may cause conflicts due to I/O operations on disk.**

#### Brew DAG Tasks Description

> --- 
> - **Bronze**: Hit the openbrewerydb API and save the JSONs returned inside the volume `/data/bronze`
> ---
> - **Silver**: Partitions data by Country and State, then save the files as parquets in `/data/silver/brewery_country={}/brewery_state={})`
> ---
> - **Gold**: Read parquets from silver to aggregate the values to return the count of breweries by type and location, print the results from each country in the screen, and save the files as parquets in `/data/gold/country={}/state={}`
> ---

### Application logs:

#### Bronze

![image](https://github.com/lucasisaacbr/brew-challenge/assets/22127369/8c3f9ea2-4000-4dab-a31f-b41ef08e4b88)


#### Silver

![image](https://github.com/lucasisaacbr/brew-challenge/assets/22127369/a94f73ab-575e-47d9-b5dd-b21c88db1bd6)


#### Gold 

![image](https://github.com/lucasisaacbr/brew-challenge/assets/22127369/f772f798-e202-4eac-9cac-ae0cebdb2666)


> If you want to play with the data, you can create a notebook in JupyterHub
> Just access: http://127.0.0.1:8888/lab?token={RANDOM_TOKEN}
> The token to access it always changes. Check the token in the logs from `docker compose up` as in the example:

![image](https://github.com/lucasisaacbr/brew-challenge/assets/22127369/08988df0-c352-47d8-b772-d01994a29b1b)
