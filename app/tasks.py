from app.celery_app import celery_app
import subprocess
import os
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def run_test_task(self, test_id):
    # Устанавливаем переменную окружения для фильтрации теста по ID
    os.environ['TEST_ID'] = str(test_id)

    # Запускаем pytest
    result = subprocess.run(
        ["pytest", "tests/test_generated.py", "-s", "--alluredir", "./allure-results", "-v"],
        capture_output=True,
        text=True
    )

    # Логируем вывод
    logger.info(f"Pytest stdout:\n{result.stdout}")
    logger.error(f"Pytest stderr:\n{result.stderr}")

    if result.returncode != 0:
        raise Exception(f"Test failed:\n{result.stdout}\n{result.stderr}")

    return result.stdout
