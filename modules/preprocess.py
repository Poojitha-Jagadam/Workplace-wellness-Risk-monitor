import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_data(filepath):
    return pd.read_csv(filepath)

def preprocess(df):
    df.fillna(df.median(numeric_only=True), inplace=True)
    df = pd.get_dummies(df, columns=['job_role'])
    scaler = MinMaxScaler()
    numeric_cols = ['heart_rate', 'blood_pressure', 'fatigue_score']
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df
