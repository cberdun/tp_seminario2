"""Stocks dag."""
import json
from datetime import datetime, timedelta
from tabnanny import verbose

import numpy as np
import pandas as pd
import requests
import logging

from airflow import AirflowException
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.task_group import TaskGroup
from sqlite_cli import SqLiteClient

STOCK_SYMBOLS = Variable.get(
    "stock_symbols",
    [
        "AAPL",
        "BABA",
        "CSCO",
        # "DHR",
        "EBAY",
        "META",
        # "goog",
        # "googl",
        # "ibm",
        # "intc",
        # "wdc",
    ],
)
CONNECTION_ID = "postgres_local"
BASE_URL = "https://www.alphavantage.co/query"
API_KEY = "TFHNYCWBD71JBSON"
STOCK_FN = "TIME_SERIES_DAILY"

SQL_DB = "/tmp/sqlite_default.db"  # This is defined in Admin/Connections
SQL_TABLE = "stocks_daily"
SQL_CREATE = f"""
CREATE TABLE IF NOT EXISTS {SQL_TABLE} (
date TEXT,
symbol TEXT,
avg_num_trades REAL,
avg_price REAL,
UNIQUE(date,symbol)
)
"""

task_logger = logging.getLogger('airflow.task').setLevel(logging.DEBUG)


def _get_stock_data(stock_symbol, **context):
    date = context["execution_date"].strftime(
        "%Y-%m-%d"
    )  # read execution date from context
    end_point = (
        f"{BASE_URL}?function={STOCK_FN}&symbol={stock_symbol}"
        f"&apikey={API_KEY}&datatype=json"
    )
    print(f"Getting data from {end_point}...")
    r = requests.get(end_point)
    data = json.loads(r.content)

    print(f"Data: {data}")

    date_col = "Date"
    open_col = "Open"
    high_col = "High"
    low_col = "Low"
    close_col = "Close"
    vol_col = "Volume"

    if "Error Message" in data:
        raise AirflowException(data["Error Message"])

    if "Time Series (Daily)" not in data:
        raise AirflowException(f"Symbol {stock_symbol} does not exist!")

    df = (
        pd.DataFrame(data["Time Series (Daily)"])
        .T.reset_index()
        .rename(
            columns={
                "index": date_col,
                "1. open": open_col,
                "2. high": high_col,
                "3. low": low_col,
                "4. close": close_col,
                "5. volume": vol_col,
            }
        )
    )
    df = df[df[date_col] == date]
    if not df.empty:
        for c in df.columns:
            if c != date_col:
                df[c] = df[c].astype(float)
    else:
        df = pd.DataFrame(
            [[date, np.nan, np.nan]],
            columns=[date_col, open_col, high_col, low_col, close_col, vol_col],
        )
    df["symbol"] = stock_symbol
    df = df[[date_col, "symbol", open_col, high_col, low_col, close_col, vol_col]]

    df.to_csv(f"/dataset/stocks/{stock_symbol}.txt", index=False)

    return df


default_args = {
    "owner": "mutt",
    "retries": 3,
    "depends_on_past": True,
    "retry_delay": timedelta(seconds=30),
}
with DAG(
    "stocks_spark",
    start_date=datetime(2022, 8, 14),
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 4 * * *",
    catchup=False,
) as dag:
    create_table_if_not_exists = PostgresOperator(
        task_id="create_table_if_not_exists",
        sql=SQL_CREATE,
        postgres_conn_id=CONNECTION_ID,
    )

    with TaskGroup(group_id=f"get_daily_data") as get_daily_data_task_group:
        for symbol in STOCK_SYMBOLS:
            get_daily_data_symbol = PythonOperator(
                task_id=f"get_{symbol}_daily_data",
                python_callable=_get_stock_data,
                op_args=[symbol],
                provide_context=True,
            )

    # spark_submit_local = SparkSubmitOperator(
    #     task_id=f"spark_submit_process_task",
    #     application="/opt/airflow/dags/spark_stocks_job.py",
    #     application_args=[f"/dataset/stocks", "/dataset/yahoo-symbols-201709.csv"],
    #     conn_id="spark_local",
    #     jars="/app/postgresql-42.1.4.jar",
    #     executor_cores=1,
    #     name='airflow-spark',
    #     executor_memory="512m",
    #     driver_memory="512m",
    #     verbose=True,
    # )

    spark_submit_local = BashOperator(
        task_id='spark_submit_process_task',
        bash_command="spark-submit   --total-executor-cores 1   --executor-memory 512m   --driver-memory 512m   --master 'spark://master:7077'   --jars /app/postgresql-42.1.4.jar   /opt/airflow/dags/spark_stocks_job.py  /dataset/stocks /dataset/yahoo-symbols-201709.csv",
    )

    create_table_if_not_exists >> get_daily_data_task_group >> spark_submit_local
