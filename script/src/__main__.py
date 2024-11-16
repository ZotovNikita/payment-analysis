import logging
from pathlib import Path

import joblib
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

from .settings import load_settings


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.StreamHandler()],
        format='[%(levelname)s] [%(asctime)s] %(message)s',
    )
    settings = load_settings()

    logging.info('- = - Загрузка моделей - = -')

    vectorizer: TfidfVectorizer = joblib.load(settings.vectorizer_path)
    label_encoder: LabelEncoder = joblib.load(settings.label_encoder_path)
    classifier: CatBoostClassifier = joblib.load(settings.classifier_path)

    logging.info('- = - Поиск файлов .tsv в директории %s - = -', settings.input_files_dir)

    for path in Path(settings.input_files_dir).glob('**/*.tsv'):

        logging.info('- = - Обработка файла %s - = -', path)

        try:
            df = pd.read_csv(path, encoding='utf-8', header=None,  names=['index', 'date', 'cash', 'description'], sep='\t')

            embeddings = vectorizer.transform(df['description'])
            embeddings_df = pd.DataFrame(embeddings.toarray(), columns=vectorizer.get_feature_names_out())

            y_pred = classifier.predict(embeddings_df)
            predicted_labels = label_encoder.inverse_transform(y_pred.ravel())

            result_df = pd.DataFrame({'index': df['index'], 'type': predicted_labels})
            result_path = str(path).removesuffix('.tsv') + '_predicted.tsv'

            logging.info('- = - Сохранение файла %s - = -', result_path)
            result_df.to_csv(result_path, sep='\t', index=False, header=False)

            logging.info('- + - Успешно - + -')
        except Exception as e:
            logging.info('- - - Ошибка - - -', exc_info=e)


if __name__ == '__main__':
    main()
