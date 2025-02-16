import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Step 1: Fetch Stock Data
def fetch_stock_data(stock_symbol, start_date, end_date):
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    return data[['Close']]

# Step 2: Preprocess Data
def preprocess_data(data):
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data)
    return scaled_data, scaler

# Step 3: Create Training & Testing Sets
def create_sequences(data, time_step=60):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

# Step 4: Build LSTM Model
def build_lstm_model():
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(60, 1)),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=25),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Step 5: Train & Predict
def train_and_predict(stock_symbol, start_date, end_date):
    # Fetch Data
    data = fetch_stock_data(stock_symbol, start_date, end_date)
    
    # Preprocess
    scaled_data, scaler = preprocess_data(data)
    
    # Create Sequences
    X, Y = create_sequences(scaled_data)
    X = X.reshape(X.shape[0], X.shape[1], 1)  # Reshape for LSTM
    
    # Split Data
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    Y_train, Y_test = Y[:train_size], Y[train_size:]
    
    # Build & Train Model
    model = build_lstm_model()
    model.fit(X_train, Y_train, epochs=20, batch_size=32, validation_data=(X_test, Y_test))
    
    # Predict
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions.reshape(-1, 1))
    Y_test_actual = scaler.inverse_transform(Y_test.reshape(-1, 1))
    
    # Plot Predictions
    plt.figure(figsize=(12, 6))
    plt.plot(Y_test_actual, label='Actual Prices')
    plt.plot(predictions, label='Predicted Prices')
    plt.legend()
    plt.title(f'{stock_symbol} Stock Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.show()

# Run Prediction
stock_symbol = input("Enter stock symbol (e.g., AAPL, TSLA): ")
start_date = "2020-01-01"
end_date = "2024-01-01"
train_and_predict(stock_symbol, start_date, end_date)
