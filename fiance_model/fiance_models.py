
import yfinance as yf
import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn
import numpy as np

# CUDA
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# QQQ 종목 데이터 다운로드 (1970년 ~ 현재)
data = yf.download('QQQ', start='1970-01-01')
data = data[['Close']]

# 데이터 정규화
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# 데이터 전처리
def create_sequences(data, seq_length=60):
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:i + seq_length]
        y = data[i + seq_length]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

# 시계열 데이터 생성 및 텐서 변환
X, y = create_sequences(data_scaled)
X_train, y_train = torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)
train_data = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

# LSTM 모델 정의 추가
class LSTMModel(nn.Module):
    def __init__(self):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=50, batch_first=True)
        self.linear = nn.Linear(50, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        y_pred = self.linear(lstm_out[:, -1])
        return y_pred

# 모델 설정
model = LSTMModel().to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


epochs = 100
for epoch in range(epochs):
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)

        optimizer.zero_grad()
        y_pred = model(X_batch)
        loss = criterion(y_pred, y_batch)
        loss.backward()
        optimizer.step()
    
    if (epoch+1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")

# 평가
model.eval()
with torch.no_grad():
    y_pred = model(X_train.to(device)).cpu().numpy()
    y_true = y_train.cpu().numpy()


y_pred = scaler.inverse_transform(y_pred)
y_true = scaler.inverse_transform(y_true)
rmse = mean_squared_error(y_true, y_pred, squared=False)
mape = mean_absolute_percentage_error(y_true, y_pred)
print(f"RMSE: {rmse}, MAPE: {mape}")
