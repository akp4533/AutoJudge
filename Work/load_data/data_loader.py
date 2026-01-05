import os
from functools import lru_cache
import pandas as pd
import json

DATA_PATH = r"C:\Users\asus\Desktop\ACM\Work\load_data\processed.parquet"

META_PATH = r"C:\Users\asus\Desktop\ACM\Work\load_data\processed_meta.json"

@lru_cache(maxsize=1)
def load_df(path: str = None):
    p = path or DATA_PATH
    if not os.path.exists(p):
        raise FileNotFoundError(f"Processed data not found at: {p}")
    return pd.read_parquet(p)

def load_meta(path: str = None):
    p = path or META_PATH
    if os.path.exists(p):
        with open(p, "r") as f:
            return json.load(f)
    return {}
