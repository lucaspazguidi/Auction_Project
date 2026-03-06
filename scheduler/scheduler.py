from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# BackgroundScheduler — para rodar em apps web (Flask, FastAPI).

# Used to store the schedule jobs
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.db')
}

scheduler = BackgroundScheduler(jobstores=jobstores)