from pathlib import Path

import pandas as pd
from sentence_transformers import SentenceTransformer

from .settings import load_settings


def main() -> None:
    settings = load_settings()
    embedder = SentenceTransformer('intfloat/multilingual-e5-large-instruct', backend='onnx', tokenizer_kwargs={'max_length': 512, 'padding': True, 'truncation': True, 'return_tensors': 'pt'})

    for path in Path(settings.input_files_dir).glob('**/*.tsv'):
        df = pd.read_csv(path, encoding='utf-8', sep='\t')

        texts = ['Привет мир', 'мир, привет']
        embeddings = embedder.encode(texts, batch_size=32, show_progress_bar=True)

        print(f'{path} -> {str(path).removesuffix('.tsv') + '_predicted.tsv'}')
        print(embedder.similarity(embeddings, embeddings))


if __name__ == '__main__':
    main()
