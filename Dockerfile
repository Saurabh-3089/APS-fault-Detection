#base machine
FROM python:3.8
#root user
USER root
#make directory to keep code
RUN mkdir /app
#copy all code files in app folder
COPY . /app/
WORKDIR /app/
#install all dependencies
RUN pip3 install -r requirements.txt
#airflow
ENV AIRFLOW_HOME ="/app/airflow"
ENV AIRFLOW_CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW_CORE_ENABLE_XCOM_PICKLING=True
#initialize DB in Airflow
RUN airflow db init
#create airflow user
RUN airflow users create  -e saurabhchauhan3089@gmail.com -f Saurabh -l Chauhan -p  admin -r Admin  -u admin
#give permission to run start.sh
RUN chmod 777 start.sh
#install AWSCLI to store 3 files model,transfromer,encoder in S3 bucket
RUN apt update -y && apt install awscli -y
#points to shell file ans starts it
ENTRYPOINT [ "/bin/sh" ]
CMD ["start.sh"]