from celery import Celery
from app.config import settings

celery_app = Celery(
    'app',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.tasks']
)

celery_app.conf.update(
    result_expires=3600,
)
