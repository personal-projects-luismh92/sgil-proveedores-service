"""Celery tasks for sending emails and logging to the Logging Microservice."""
import os
import json
import logging
import requests
from common_for_services.notification.smtp import EmailService
from common_for_services.tasks.celery_worker import celery

LOGGING_SERVICE_URL = os.getenv("LOGGING_SERVICE_URL",
                                "http://localhost:8090/logs")


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("proveedores_log")
headers = {"Content-Type": "application/json"}


@celery.task
def send_email_task(to_email: str, subject: str, body: str):
    """Send an email asynchronously using Celery."""
    try:
        logger.info("send_email_task ---------------------------")
        email = EmailService()
        email.send_email(subject, body)
        return f"Email sent successfully to {to_email}"

    except Exception as e:
        return f"Failed to send email: {str(e)}"


@celery.task
def log_to_logging_service_task(log_data: dict):
    """Send logs asynchronously to the Logging Microservice."""
    try:
        logger.info("log_to_logging_service_task ---------------------------")
        log_data["service_name"] = "sgil-proveedores-service"
        del log_data["package"]
        del log_data["module"]
        logger.info("Sending log data: %s", json.dumps(log_data, indent=4))

        response = requests.post(
            LOGGING_SERVICE_URL, json=log_data, headers=headers)
        response.raise_for_status()
        return f"Log stored successfully: {response.json()}"
    except requests.exceptions.RequestException as e:
        return f"Failed to log data: {str(e)}"


# celery -A celery_worker.celery_config.celery flower --broker=redis://localhost:6379/0
# celery -A celery_worker.celery_config.celery worker --loglevel=info --concurrency=4 -Q email_queue,logging_queue
# docker run -p 6379:6379 --name broker-redis -d redis
# celery -A celery_worker.celery_config.celery result 4fb60c16-e900-47a5-878b-d3976657abd0
