FROM jupyter/pyspark-notebook
COPY ../.. /home/lisaac/work
USER root
RUN apt-get update -y && apt-get upgrade -y  \
    && apt-get install openssh-server -y
COPY ./sshd_config  /etc/ssh/sshd_config
RUN service ssh start
RUN service ssh restart
RUN mkdir -p /data/bronze /data/silver /data/gold
RUN chmod 777 /data /data/bronze /data/silver /data/gold # set permission to write files
EXPOSE 22
EXPOSE 4041
EXPOSE 4040
EXPOSE 8888