import asyncio

from src.utils.nlu import generate_prediction


class PredictBatch:
    async def __call__(self, texts: list[str]) -> list[str]:
        payment_preds = await asyncio.to_thread(
            generate_prediction,
            texts=texts,
        )

        return payment_preds.tolist()
