from sqlalchemy import Column, Integer, String, ForeignKey, Table, JSON, Text
from sqlalchemy.orm import relationship
from app.database import Base

test_steps_association = Table(
    'test_steps',
    Base.metadata,
    Column('test_id', Integer, ForeignKey('tests.id')),
    Column('step_id', Integer, ForeignKey('steps.id')),
    Column('order', Integer)
)

class Endpoint(Base):
    __tablename__ = 'endpoints'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True)
    url: str = Column(String)
    method: str = Column(String)
    headers: dict | None = Column(JSON, nullable=True)
    query_params: dict | None = Column(JSON, nullable=True)
    body: dict | None = Column(JSON, nullable=True)

class Step(Base):
    __tablename__ = 'steps'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    action: str = Column(String)  # "request", "assertion", etc.
    endpoint_id: int | None = Column(Integer, ForeignKey('endpoints.id'), nullable=True)
    parameters: dict | None = Column(JSON, nullable=True)
    endpoint = relationship('Endpoint')
    allure_step: str | None = Column(String, nullable=True)

class DatabaseTest(Base):
    __tablename__ = "tests"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    description: str | None = Column(Text, nullable=True)
    steps = relationship('Step', secondary=test_steps_association, order_by='test_steps.c.order')
    allure_feature: str | None = Column(String, nullable=True)
    allure_story: str | None = Column(String, nullable=True)
    allure_epic: str | None = Column(String, nullable=True)
    allure_description: str | None = Column(Text, nullable=True)
