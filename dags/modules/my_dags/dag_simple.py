from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


class DagSimple(DAG):

    def __init__(self, dag_id: str) -> None:
        default_args = {'start_date': datetime.utcnow()}
        super().__init__(dag_id=dag_id,
                         default_args=default_args)

    def op(self, f: 'func') -> PythonOperator:
        return PythonOperator(task_id=f.__name__,
                              python_callable=f,
                              dag=self)
