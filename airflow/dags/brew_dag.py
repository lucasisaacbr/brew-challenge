from datetime import timedelta, datetime
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime.now() - timedelta(minutes=20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(dag_id='brew_dag',
          default_args=default_args,
          schedule_interval='*/5 * * * *',
          dagrun_timeout=timedelta(seconds=120))

bronze_bash = """
python /home/lisaac/work/bronze_extraction.py 
"""
bronze_task = SSHOperator(
    ssh_conn_id='brew-notebooks',
    task_id='bronze_task',
    command=bronze_bash,
    dag=dag)

silver_bash = """
python /home/lisaac/work/silver_transformation.py
"""
silver_task = SSHOperator(
    ssh_conn_id='brew-notebooks',
    task_id='silver_task',
    command=silver_bash,
    dag=dag)

gold_bash = """
python /home/lisaac/work/gold_transformation.py
"""
gold_task = SSHOperator(
    ssh_conn_id='brew-notebooks',
    task_id='gold_task',
    command=gold_bash,
    dag=dag)

bronze_task >> silver_task >> gold_task
