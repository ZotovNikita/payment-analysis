import json
import pyarrow as pa
import requests
import streamlit as st
import pandas as pd

from settigns import Settings


async def upload():
    st.subheader("Загрузка данных")
    tsv_file = st.file_uploader("Загрузите TSV файл", type=["tsv"])
    path = Settings()
    path = path.backend_base_url
    if tsv_file is not None:
        data = pd.read_csv(tsv_file, encoding='utf-8', header=None,  names=['index', 'date', 'cash', 'description', 'type'], sep='\t', index_col=0)

        if st.button('Получить предсказание'):
            url = f'{path}/predict/batch'
            data = data['description']
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, data=json.dumps(list(data))).json()

            data['тип платежа'] = response
            st.session_state['predicted_data'] = response
            st.subheader("Данные:")

            st.write(data)
