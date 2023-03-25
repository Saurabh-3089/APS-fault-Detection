#!bin/sh
#launch airflow scheduler
nohup airflow scheduler &
#webserver gives an application
airflow webserver
#sh is bash shell script
