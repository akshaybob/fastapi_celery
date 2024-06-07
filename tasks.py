import time
from sqlalchemy.orm import Session
from datetime import datetime
from models import Task, LegitimateSeller, SessionLocal
import uuid
import json
import urllib.request
from celery_config import celery
import logging


@celery.task(name='scheduler')
def scheduler():
    logging.info('schedular called')
    db: Session = SessionLocal()
    try:
        new_task = Task(
            run_id=str(uuid.uuid4()),
            date=datetime.utcnow().date(),
            status='SCHEDULED'
        )
        db.add(new_task)
        db.commit()
        logging.info(f"Scheduled new task with run_id: {new_task.run_id}")
    except Exception as e:
        db.rollback()
        logging.info(f"Failed to schedule new task: {e}")
    finally:
        db.close()


@celery.task(name='executor')
def executor():
    db: Session = SessionLocal()
    try:
        task = db.query(Task).filter_by(status='SCHEDULED').first()
        if task:
            task.status = 'STARTED'
            task.started_at = datetime.utcnow()
            db.commit()
            logging.info(f"Started task with run_id: {task.run_id}")

            with open('sites.json') as f:
                sites = json.load(f)["sites"]
                logging.info(f"Processing sites: {sites}")

            for domain in sites:
                url = f"https://{domain}/ads.txt"
                try:
                    time.sleep(5)
                    with urllib.request.urlopen(url) as response:
                        if response.getcode() == 200:
                            for line in response.read().decode('utf-8').splitlines():
                                parts = line.split(',')
                                if len(parts) >= 3:
                                    ssp_domain_name, publisher_id, seller_relationship = parts[:3]
                                    tag_id = parts[3] if len(parts) > 3 else None
                                    new_seller = LegitimateSeller(
                                        site=domain,
                                        ssp_domain_name=ssp_domain_name.strip(),
                                        publisher_id=publisher_id.strip(),
                                        seller_relationship=seller_relationship.strip(),
                                        date=datetime.utcnow().date(),
                                        run_id=task.run_id
                                    )
                                    db.add(new_seller)
                except Exception as e:
                    logging.info(f"An error occurred processing {domain}: {e}")

            task.status = 'FINISHED'
            task.finished_at = datetime.utcnow()
        else:
            logging.info("No scheduled tasks found.")
    except Exception as e:
        db.rollback()
        logging.info(f"Failed to process task: {e}")
    finally:
        try:
            db.commit()
        except Exception as e:
            logging.info(f"Failed to commit changes to the database: {e}")
        finally:
            db.close()