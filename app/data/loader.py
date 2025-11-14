import pickle
import os
import pandas as pd
import xgboost as xgb
from pathlib import Path
from dotenv import load_dotenv
from lime.lime_tabular import LimeTabularExplainer
from sklearn.model_selection import train_test_split
import numpy as np

load_dotenv()

FILES_PATH = Path(os.getenv("FILES_PATH"))
DOWNLOADS_PATH = Path(os.getenv("DOWNLOADS_PATH"))

with open(FILES_PATH / "encoders.pkl", "rb") as f:
    encoders_dict = pickle.load(f)
nomes_colunas_categoricas = list(encoders_dict.keys())

df = pd.read_csv(FILES_PATH / "df_tratado.csv")

model = xgb.XGBClassifier()
model.load_model(FILES_PATH / "model.json")

X_df = df[df.columns.difference(['SITUACAO'])]
Y_df = df['SITUACAO']

train_X, test_X, train_y, test_y = train_test_split(X_df, Y_df, test_size=0.33, random_state=42)

X_train_np = np.array(train_X)
X_test_np = np.array(test_X)
feature_names = train_X.columns if isinstance(train_X, pd.DataFrame) else [f"feature_{i}" for i in range(train_X.shape[1])]
class_names = np.unique(train_y)

explainer = LimeTabularExplainer(
    training_data=X_train_np,
    feature_names=feature_names,
    class_names=class_names,
    mode='classification'
)