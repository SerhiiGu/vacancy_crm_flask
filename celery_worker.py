from celery import Celery
from email_lib import EmailWrapper
from models import EmailCredentials
import al_db
import os


rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')

app = Celery('celery_worker', broker=f'pyamqp://guest@{rabbitmq_host}//')


@app.task()
def send_mail(id_email_credentials, recipient, message):
    email_creds = al_db.db_session.query(EmailCredentials).get(id_email_credentials)
    email_wrapper = EmailWrapper(**email_creds.get_mandatory_fields())
    email_wrapper.send_email(recipient, message)
