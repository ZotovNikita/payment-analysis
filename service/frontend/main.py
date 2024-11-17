import asyncio

import streamlit as st
from streamlit_option_menu import option_menu

from report import report
from upload import upload


async def main():
    if 'predicted_data' not in st.session_state:
        st.session_state['predicted_data'] = []

    st.title("Автоматизация разбора платежей")
    selected = option_menu(None, ["Загрузка данных", "Отчет"],
                            icons=['cloud-upload', 'file-earmark-text-fill'],
                            menu_icon="cast", default_index=0, orientation="horizontal")

    if selected == 'Загрузка данных':
        await upload()
    elif selected == 'Отчет':
        await report()

if __name__ == '__main__':
    asyncio.run(main())


