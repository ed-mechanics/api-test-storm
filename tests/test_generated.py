import pytest
import os
from app.models import DatabaseTest as TestModel
from app.test_runner import MyTestRunner
from app.database import SessionLocal

def pytest_generate_tests(metafunc):
    if "test_data" in metafunc.fixturenames:
        test_id = os.getenv('TEST_ID')
        db_session = SessionLocal()
        if test_id:
            tests = db_session.query(TestModel).filter(TestModel.id == int(test_id)).all()
        else:
            tests = db_session.query(TestModel).all()
        db_session.close()

        ids = [f"test_{test.id}" for test in tests]
        metafunc.parametrize("test_data", tests, ids=ids)

def test_generated(test_data):
    with SessionLocal() as db_session:
        test_data = db_session.merge(test_data)
        test_runner = MyTestRunner(db_session)
        test_runner.run_test(test_data)
