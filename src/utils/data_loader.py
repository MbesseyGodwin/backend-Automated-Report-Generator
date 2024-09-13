# backend/src/utils/data_loader.py

import pandas as pd

class DataLoader:
    @staticmethod
    def load_data_from_csv(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)
