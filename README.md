# fastapi_celery
POC for fastapi celery webscraping



Database setup:
 create .env file in same dir location
 
 add env variable as below:

 
  CELERY_BROKER_URL=redis://localhost:6379/1
  
  CELERY_RESULT_BACKEND=redis://localhost:6379/1
  
  DATABASE_URL=postgresql://postgres:root@localhost:5432/postgres

 
creating Virtual Environment:
py -m venv venv



activating env

.\venv\Scripts\activate


installing requirments:
pip insatll -r requirements.txt


for run celery task:-


terminal 1:

  celery -A celery_app worker -Q scheduler,executor --loglevel=info 

terminal 2:

  celery -A celery_app beat --loglevel=info


terminal 3: running application

  py main.py 
