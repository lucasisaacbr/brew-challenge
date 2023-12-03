FROM jupyter/pyspark-notebook
COPY . /home/lisaac/work
USER root
RUN mkdir -p /data/bronze /data/silver /data/gold
RUN chmod 777 /data /data/bronze /data/silver /data/gold


#docker run -it --rm \
#    -p 8888:8888 \
#    -p 4040:4040 \
#    -p 4041:4041 \
#    --user root \
#    -e NB_USER="lisaac" \
#    -e CHOWN_HOME=yes \
#    -e GRANT_SUDO=yes \
#    -w "/home/lisaac" \
#    -v "${PWD}":/home/lisaac/work \
#    lisaac/test