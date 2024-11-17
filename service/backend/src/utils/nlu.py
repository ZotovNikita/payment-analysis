import joblib
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

from src.settings import load_settings


__all__ = [
    'vectorizer',
    'label_encoder',
    'classifier',
    'generate_embeddings_df',
    'generate_prediction',
]

settings = load_settings()

vectorizer: TfidfVectorizer = joblib.load(settings.vectorizer_path)
label_encoder: LabelEncoder = joblib.load(settings.label_encoder_path)
classifier = CatBoostClassifier()
classifier.load_model(settings.classifier_path)


def generate_embeddings_df(texts: list[str] | np.ndarray) -> pd.DataFrame:
    embeddings = vectorizer.transform(texts)
    return pd.DataFrame(embeddings.toarray(), columns=vectorizer.get_feature_names_out())


def generate_prediction(texts: list[str] | np.ndarray) -> np.ndarray:
    embeddings_df = generate_embeddings_df(texts)
    y_pred = classifier.predict(embeddings_df)
    return label_encoder.inverse_transform(y_pred.ravel())
