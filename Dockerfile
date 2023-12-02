FROM jupyter/pyspark-notebook
COPY . /home/jovyan/work

#docker run --detach -p 8888:8888 -p 4040:4040 -p 4041:4041 -v "${PWD}":/home/jovyan/work jupyter/pyspark-notebook