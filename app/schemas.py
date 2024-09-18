from pydantic import BaseModel, Field
from typing import Any

class EndpointBase(BaseModel):
    name: str
    url: str
    method: str
    headers: dict[str, Any] = Field(default_factory=dict)
    query_params: dict[str, Any] = Field(default_factory=dict)
    body: dict[str, Any] = Field(default_factory=dict)

class EndpointCreate(EndpointBase):
    pass

class Endpoint(EndpointBase):
    id: int

    class Config:
        from_attributes = True

class StepBase(BaseModel):
    name: str
    action: str
    endpoint_id: int | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    allure_step: str | None = None

class StepCreate(StepBase):
    pass

class Step(StepBase):
    id: int
    endpoint: Endpoint | None = None

    class Config:
        from_attributes = True

class TestBase(BaseModel):
    name: str
    description: str | None = None
    steps: list[int]
    allure_feature: str | None = None
    allure_story: str | None = None
    allure_epic: str | None = None
    allure_description: str | None = None

class TestCreate(TestBase):
    pass

class Test(TestBase):
    id: int
    steps: list[Step]

    class Config:
        from_attributes = True
