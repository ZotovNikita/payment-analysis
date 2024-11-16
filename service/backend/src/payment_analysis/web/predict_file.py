import asyncio
import pandas as pd
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO, StringIO

from src.utils.nlu import generate_prediction


class PredictFile:
    async def __call__(self, file: UploadFile = File(...)) -> None:
        try:
            contents = await file.read()
        finally:
            await file.close()

        def proccess(content: bytes) -> str:
            data = BytesIO(content)
            csv = pd.read_csv(data, encoding='utf-8', header=None,  names=['index', 'date', 'cash', 'description'], sep='\t')

            preds = generate_prediction(csv['description'])

            preds_df = pd.DataFrame({'index': csv['index'], 'type': preds})

            stream = StringIO()
            preds_df.to_csv(stream, sep='\t', index=False, header=False)

            return stream.getvalue()

        data = await asyncio.to_thread(proccess, content=contents)

        return StreamingResponse(
            iter([data]),
            media_type='text/csv',
            headers={
                'Content-Disposition': 'attachment;filename=submission.csv',
            }
        )
