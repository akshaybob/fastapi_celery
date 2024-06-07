# fastapi_celery
POC for fastapi celery webscraping

Database setup:
need to change URL in models.py for database acess

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
