import pickle
import os
import pandas as pd
import xgboost as xgb
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

FILES_PATH = Path(os.getenv("FILES_PATH"))

with open(FILES_PATH / "encoders.pkl", "rb") as f:
    encoders_dict = pickle.load(f)

df = pd.read_csv(FILES_PATH / "df_tratado.csv")

model = xgb.XGBClassifier()
model.load_model(FILES_PATH / "model.json")
