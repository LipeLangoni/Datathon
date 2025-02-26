import mlflow
import mlflow.keras
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
import yfinance as yf
import pandas as pd
import joblib
import pickle
import os
import boto3


s3 = boto3.client('s3')

def save_to_s3(file_name, bucket_name, file_content):
    """Helper function to save a file to S3."""
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)


# Lambda handler
def lambda_handler(event, context):
    tickers = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'ABEV3.SA']
    
    for ticker in tickers:
        X_train, X_test, y_train, y_test, scaler = data_preparation(ticker)
        train_model(X_train, y_train, X_test, y_test, ticker, scaler)

    return {
        'statusCode': 200,
        'body': 'Model training completed and tracked with MLflow for all tickers.'
    }

def create_dataset(data, time_step=60):
    X, y = [], []
    for i in range(time_step, len(data)):
        X.append(data[i-time_step:i, 0])  
        y.append(data[i, 0])              
    return np.array(X), np.array(y)

def data_preparation(ticker):
    start_date = '2018-01-01'
    end_date = '2024-07-20'

    df = yf.download(ticker, start=start_date, end=end_date)
    df = df[['Close']]

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['Close']])

    time_step = 60
    X, y = create_dataset(scaled_data, time_step)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    return X_train, X_test, y_train, y_test, scaler

def train_model(X_train, y_train, X_test, y_test, ticker, scaler):
    model = Sequential()

    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))  

    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Start MLflow run
    mlflow.set_tracking_uri("http://mlflow-url.amazonaws.com")
    with mlflow.start_run():
        # Log model parameters
        mlflow.log_param("units", 50)
        mlflow.log_param("dropout_rate", 0.2)
        mlflow.log_param("batch_size", 32)
        mlflow.log_param("epochs", 10)

        history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

        for epoch in range(10):
            mlflow.log_metric("loss", history.history['loss'][epoch], step=epoch)

      
        mlflow.keras.log_model(model, f"{ticker}_model")

        model_file_path = "/tmp/model.h5"
        model.save(model_file_path)  
        
        with open(model_file_path, 'rb') as model_file:
            model_content = model_file.read()
        model_s3_key = f"models/{ticker}_model.h5"
        save_to_s3(model_s3_key, "lstm_bucket", model_content)
        
        scaler_file_path = "/tmp/scaler.pkl"
        joblib.dump(scaler, scaler_file_path)  
        
        with open(scaler_file_path, 'rb') as scaler_file:
            scaler_content = scaler_file.read()
        scaler_s3_key = f"scalers/{ticker}_scaler.pkl"
        save_to_s3(scaler_s3_key, "lstm_bucket", scaler_content)

        mlflow.log_artifact(model_s3_key)
        mlflow.log_artifact(scaler_s3_key)

    return model
