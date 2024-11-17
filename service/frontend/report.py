import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


async def report():
    if 'predicted_data' in st.session_state:
        class_names = list(set(st.session_state['predicted_data']))
        y_pred = st.session_state['predicted_data']

        # Распределение классов
        st.subheader("Распределение классов")
        class_distribution = pd.DataFrame(
            {'Class': class_names, 'Count': [list(y_pred).count(i) for i in range(len(class_names))]})
        fig, ax = plt.subplots()
        sns.barplot(x='Class', y='Count', data=class_distribution, ax=ax)
        st.pyplot(fig)
    else:
        st.write('Загрузите данные ...')
