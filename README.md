# fastapi_celery
POC for fastapi celery webscraping

system requirement: 
1.redis installed with system
2.postgres database

Database setup:
 1.create .env file in same dir location
 (sample is given in repository)
 2.add env variable as below:

CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1
DATABASE_URL=postgresql://postgres:root@localhost:5432/postgres

 
creating Virtual Environment:
py -m venv venv


activating env:

.\venv\Scripts\activate


installing requirments:
pip insatll -r requirements.txt


for run celery task:-


terminal 1:

  celery -A celery_app worker  -l info -P eventlet 

terminal 2:

  celery -A celery_app beat --loglevel=info


terminal 3: running application

  py main.py 
