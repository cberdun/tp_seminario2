FROM apache/airflow:2.3.3

USER root

RUN apt-get update -y && \
    apt-get install -y default-jdk

ENV JAVA_HOME='/usr/lib/jvm/java-11-openjdk-amd64'
ENV PATH=$PATH:$JAVA_HOME/bin

USER airflow

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV AIRFLOW_CONN_POSTGRES_LOCAL=postgres://workshop:w0rkzh0p@postgres:5432/workshop
# ENV AIRFLOW_CONN_SPARK_LOCAL=spark://master:7077

# ENV SPARK_HOME='/opt/spark'
# ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin