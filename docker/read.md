### Building the  Image
This image contains the pyspark-jupyter notebooks. But also some configurations were included to support SSH connections.

To build run:

```docker build -t {YOUR_DOCKER_HUB_USERNAME}/pyspark-notebook:latest ./docker```

ps: the last parameter `./docker` should be executed in the root folder of this repo.