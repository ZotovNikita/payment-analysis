from typing import AsyncGenerator, get_type_hints

from fastapi import FastAPI

from src.ioc import ioc
from src.settings import Settings
from .web import PredictFile, PredictBatch, PredictCategory, FitClassification


__all__ = ['payment_analysis_plugin']


async def payment_analysis_plugin(settings: Settings) -> AsyncGenerator:
    fastapi = ioc.resolve(FastAPI)

    task_storage = {}

    fit_classification_view = FitClassification(settings, task_storage)
    fastapi.add_api_route(
        path='/fit',
        name='Дообучить классификатор',
        tags=['Fit'],
        methods=['POST'],
        endpoint=fit_classification_view.__call__,
        response_model=get_type_hints(fit_classification_view.__call__)['return'],
    )

    predict_category_view = PredictCategory()
    fastapi.add_api_route(
        path='/predict',
        name='Предсказать категорию платежа',
        tags=['Predict'],
        methods=['POST'],
        endpoint=predict_category_view.__call__,
        response_model=get_type_hints(predict_category_view.__call__)['return'],
    )

    predict_batch_view = PredictBatch()
    fastapi.add_api_route(
        path='/predict/batch',
        name='Предсказать категории платежей в батче',
        tags=['Predict'],
        methods=['POST'],
        endpoint=predict_batch_view.__call__,
        response_model=get_type_hints(predict_batch_view.__call__)['return'],
    )

    predict_file_view = PredictFile()
    fastapi.add_api_route(
        path='/predict/file',
        name='Получить предсказания категорий платежей по данным из файла tsv',
        tags=['Predict'],
        methods=['POST'],
        endpoint=predict_file_view.__call__,
        response_model=get_type_hints(predict_file_view.__call__)['return'],
    )

    yield
