import asyncio

from src.utils.nlu import generate_prediction
from ..models import PredictPaymentCategoryRequest, PredictPaymentCategoryResponse


class PredictCategory:
    async def __call__(self, payment: PredictPaymentCategoryRequest) -> PredictPaymentCategoryResponse:
        payment_preds = await asyncio.to_thread(
            generate_prediction,
            texts=[payment.purpose],
        )

        return PredictPaymentCategoryResponse(
            id=payment.id,
            date=payment.date,
            cash=payment.cash,
            purpose=payment.purpose,
            category=payment_preds[0],
        )
