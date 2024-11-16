from pydantic import BaseModel


class PredictPaymentCategoryRequest(BaseModel):
    id: str | None = None
    date: str | None = None
    cash: float | None = None
    purpose: str


class PredictPaymentCategoryResponse(BaseModel):
    id: str | None = None
    date: str | None = None
    cash: float | None = None
    purpose: str
    category: str
