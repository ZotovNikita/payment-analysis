from pathlib import Path

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
    'continue_training',
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


def continue_training(existing_model_path: Path, save_path: Path, X_text: pd.Series, y_text: pd.Series, verbose: bool):
    X_new = vectorizer.transform(X_text)
    X_new = pd.DataFrame(X_new.toarray(), columns=vectorizer.get_feature_names_out())

    y_new = label_encoder.transform(y_text)

    classifier.fit(
        X_new, y_new,
        init_model=existing_model_path,
        verbose=verbose,
        early_stopping_rounds=50,
    )

    joblib.dump(classifier, save_path)
