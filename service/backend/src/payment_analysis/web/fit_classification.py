from uuid import uuid4

import asyncio
import pandas as pd
from fastapi import File, UploadFile
from io import BytesIO

from src.settings import Settings
from src.utils.nlu import continue_training


class FitClassification:
    def __init__(self, settings: Settings, task_storage: dict[str, asyncio.Task]) -> None:
        self._settings = settings
        self._task_storage = task_storage

    async def __call__(self, train_file: UploadFile = File(...)) -> dict:
        try:
            contents = await train_file.read()
        finally:
            await train_file.close()

        def proccess(content: bytes) -> str:
            data = BytesIO(content)
            train_df = pd.read_csv(data, encoding='utf-8', header=None,  names=['X', 'y'], sep='\t', dtype=str)
            continue_training(self._settings.classifier_path, self._settings.classifier_path, train_df['X'].values, train_df['y'].values, verbose=True)

        uid = str(uuid4())
        task = asyncio.create_task(asyncio.to_thread(proccess, content=contents), name=uid)
        self._task_storage[uid] = task
        task.add_done_callback(lambda t: self._task_storage.pop(uid))

        return {'task_id': uid}
