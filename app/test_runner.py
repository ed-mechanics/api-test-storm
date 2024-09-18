import os

import allure
import requests
from allure_commons._allure import attach
from allure_commons.lifecycle import AllureLifecycle
from allure_commons.types import AttachmentType
from sqlalchemy.orm import Session

from app import models


class MyTestRunner:
    def __init__(self, db: Session):
        self.db = db
        self.session = requests.Session()
        self.response_store = {}
        self.allure_results_dir = os.getenv('ALLURE_RESULTS_DIR', './allure-results')
        self.lifecycle = AllureLifecycle()
        self.lifecycle._results_dir = self.allure_results_dir

    def run_test(self, test: models.DatabaseTest):
        # Устанавливаем метаданные Allure
        if not test:
            raise ValueError("Test not found")

        if test.allure_epic:
            allure.dynamic.epic(test.allure_epic)
        if test.allure_feature:
            allure.dynamic.feature(test.allure_feature)
        if test.allure_story:
            allure.dynamic.story(test.allure_story)
        if test.allure_description:
            allure.dynamic.description(test.allure_description)
        allure.dynamic.title(test.name or f"Test {test.id}")

        for step in test.steps:
            self.execute_step(step)

    def execute_step(self, step: models.Step):
        allure_step_name = step.allure_step or step.name
        with allure.step(allure_step_name):
            if step.action == "request":
                self.perform_request(step)
            elif step.action == "assertion":
                self.perform_assertion(step)
            else:
                raise ValueError(f"Unknown action: {step.action}")

    def perform_request(self, step: models.Step):
        endpoint = step.endpoint
        method = endpoint.method.lower()
        url = endpoint.url
        headers = endpoint.headers or {}
        params = endpoint.query_params or {}
        data = endpoint.body or {}

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data
        )

        # Сохраняем ответ для последующих шагов
        self.response_store[step.id] = response

        # Приложение запроса и ответа к отчету
        allure.attach(
            body=str(response.request.__dict__),
            name="Request",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            body=response.text,
            name="Response",
            attachment_type=allure.attachment_type.TEXT
        )

    def perform_assertion(self, step: models.Step):
        parameters = step.parameters
        target_step_id = parameters.get("target_step_id")
        assertion_type = parameters.get("assertion_type")
        expected_value = parameters.get("expected_value")

        target_response = self.response_store.get(target_step_id)
        if not target_response:
            raise ValueError(f"No response found for step {target_step_id}")

        if assertion_type == "status_code":
            assert target_response.status_code == expected_value, f"Expected status code {expected_value}, got {target_response.status_code}"
        elif assertion_type == "json_body":
            json_path = parameters.get("json_path")
            # Разбиваем путь на ключи
            keys = json_path.split('.')
            value = target_response.json()
            for key in keys:
                value = value.get(key)
                if value is None:
                    break
            actual_value = value
            assert actual_value == expected_value, f"Expected value at '{json_path}' to be '{expected_value}', got '{actual_value}'"
            # Добавляем значение в отчет Allure
            allure.attach(
                body=f"Actual value at '{json_path}': {actual_value}",
                name="Assertion Result",
                attachment_type=allure.attachment_type.TEXT
            )
        else:
            raise ValueError(f"Unknown assertion type: {assertion_type}")

