FROM jupyter/pyspark-notebook
COPY . /home/lisaac/work
USER root
RUN apt-get update -y && apt-get upgrade -y  \
    && apt-get install openssh-server -y
COPY sshd_config  /etc/ssh/sshd_config
RUN mkdir -p /data/bronze /data/silver /data/gold
RUN chmod 777 /data /data/bronze /data/silver /data/gold # set permission to write files
RUN pip install pyspark
RUN service ssh start
RUN service ssh restart
RUN chown -R ${NB_USER} /home/${NB_USER}
EXPOSE 22
EXPOSE 4041
EXPOSE 4040
EXPOSE 8888