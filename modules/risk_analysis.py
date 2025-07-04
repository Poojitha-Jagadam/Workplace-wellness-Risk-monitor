from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
import pandas as pd

def detect_anomalies(df, features):
    iso = IsolationForest(contamination=0.2, random_state=42)
    df['anomaly'] = iso.fit_predict(df[features])
    df['is_anomaly'] = df['anomaly'] == -1
    return df

def cluster_risks(df, features, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['risk_group'] = kmeans.fit_predict(df[features])
    return df
