# Pipelines de datos con Airflow + Apache Spark + Postgres + Docker

## Pre-requisitos

* Docker
* Docker compose

```
apt-get install docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
docker --version
```

## Clonado del Repositorio

Clonar el repositorio:

```shell
git clone git@github.com:MuttData/bigdata-workshop-es.git
git switch airflow-spark-data-pipelines
cd bigdata-workshop-es
```

Iniciar las herramientas:

```shell
./control-env.sh start
```

## Acceder a las consolas web

* Airflow: http://localhost:9090
* Spark master: http://localhost:8080

## Acceder a la base de datos

```shell
./control-env.sh psql
```




