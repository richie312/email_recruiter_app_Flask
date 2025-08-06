from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now()
    'email': ['richie.chatterjee31@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def my_python_function():
    """
    Write your business logic here
    """
    pass

with DAG('my_dag', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:

    python_task = PythonOperator(
        task_id='my_python_task',
        python_callable=my_python_function
    )

    email_task = EmailOperator(
        task_id='send_email',
        to='richie.chatterjee31@gmail.com',
        subject='Airflow Alert',
        html_content='Your DAG has completed successfully.'
    )

    python_task >> email_task