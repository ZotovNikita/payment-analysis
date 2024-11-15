from pathlib import Path

import pandas as pd

from .settings import load_settings


if __name__ == '__main__':
    settings = load_settings()

    for path in Path(settings.input_files_dir).glob('**/*.tsv'):
        df = pd.read_csv(path, encoding='utf-8', sep='\t')
        print(path)
        print(df)
