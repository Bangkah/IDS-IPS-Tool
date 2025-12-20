import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from fastapi import APIRouter, Depends


router = APIRouter()

# Dummy: Load log data for analytics (replace with real log source)
def load_log_data():
    # Simulate: 100 days, normal + 3 outliers
    np.random.seed(42)
    days = pd.date_range(end=pd.Timestamp.today(), periods=100)
    attacks = np.random.poisson(10, size=100)
    attacks[20] = 50  # anomaly
    attacks[70] = 40  # anomaly
    attacks[90] = 60  # anomaly
    df = pd.DataFrame({'date': days, 'attacks': attacks})
    return df

@router.get('/api/analytics/anomaly')
async def anomaly_detection():
    df = load_log_data()
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = model.fit_predict(df[['attacks']])
    anomalies = df[df['anomaly'] == -1][['date', 'attacks']]
    return {
        'dates': df['date'].dt.strftime('%Y-%m-%d').tolist(),
        'attacks': df['attacks'].tolist(),
        'anomalies': anomalies.to_dict(orient='records')
    }

@router.get('/api/analytics/trend')
async def attack_trend():
    df = load_log_data()
    trend = df['attacks'].rolling(window=7, min_periods=1).mean().tolist()
    return {
        'dates': df['date'].dt.strftime('%Y-%m-%d').tolist(),
        'attacks': df['attacks'].tolist(),
        'trend': trend
    }

@router.get('/api/analytics/predict')
async def predict_attacks():
    df = load_log_data()
    # Simple forecast: last value + noise
    last = df['attacks'].iloc[-1]
    pred = [int(last + np.random.normal(0, 2)) for _ in range(7)]
    return {
        'future_days': [(pd.Timestamp.today() + pd.Timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1,8)],
        'forecast': pred
    }
