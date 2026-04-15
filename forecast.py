import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from sklearn.linear_model import LinearRegression

file_path = "THROUGHPUT & CAPACITY STABILITYy.xlsx"
df = pd.read_excel(file_path)

print("Raw Data:")
print(df.head())

df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Extract date only
df['Date'] = df['Timestamp'].dt.date

# Aggregate daily production per plant
df_daily = df.groupby(['Plant', 'Date'])['ProductionUnits'].sum().reset_index()

# Convert Date back to datetime
df_daily['Date'] = pd.to_datetime(df_daily['Date'])

print("\nDaily Aggregated Data:")
print(df_daily.head())

plant_name = df_daily['Plant'].unique()[0]
plant_df = df_daily[df_daily['Plant'] == plant_name].copy()

plant_df = plant_df.sort_values('Date')
plant_df.set_index('Date', inplace=True)

print(f"\nUsing Plant: {plant_name}")

train = plant_df[:-14]
test = plant_df[-14:]

# Naive forecast (last value)
baseline_pred = [train['ProductionUnits'].iloc[-1]] * len(test)

for lag in range(1, 8):
    plant_df[f'lag_{lag}'] = plant_df['ProductionUnits'].shift(lag)

plant_df.dropna(inplace=True)

train = plant_df[:-14]
test = plant_df[-14:]

# Features
features = [f'lag_{i}' for i in range(1, 8)]

X_train = train[features]
y_train = train['ProductionUnits']

X_test = test[features]
y_test = test['ProductionUnits']

model = LinearRegression()
model.fit(X_train, y_train)

ml_pred = model.predict(X_test)

def mape(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100

baseline_mape = mape(test['ProductionUnits'], baseline_pred)
ml_mape = mape(y_test, ml_pred)

print("\n📊 RESULTS")
print("Baseline MAPE:", baseline_mape)
print("ML Model MAPE:", ml_mape)

plt.figure(figsize=(10, 5))

plt.plot(test.index, test['ProductionUnits'], label='Actual')
plt.plot(test.index, baseline_pred, label='Baseline')
plt.plot(test.index, ml_pred, label='ML Model')

plt.legend()
plt.title(f"Forecast for {plant_name}")
plt.xlabel("Date")
plt.ylabel("Production Units")

plt.show()

future_preds = []

last_values = plant_df['ProductionUnits'].values[-7:]

for i in range(14):
    input_data = last_values[-7:].reshape(1, -1)
    pred = model.predict(input_data)[0]
    
    future_preds.append(pred)
    last_values = np.append(last_values, pred)

print("\n🔮 Next 14 Days Forecast:")
print(future_preds)

print("\n📊 MAPE for All Plants")

results = []

for plant in df_daily['Plant'].unique():
    temp_df = df_daily[df_daily['Plant'] == plant].copy()
    temp_df.set_index('Date', inplace=True)
    
    # Create lag features
    for lag in range(1, 8):
        temp_df[f'lag_{lag}'] = temp_df['ProductionUnits'].shift(lag)
    
    temp_df.dropna(inplace=True)
    
    train = temp_df[:-14]
    test = temp_df[-14:]
    
    X_train = train[[f'lag_{i}' for i in range(1, 8)]]
    y_train = train['ProductionUnits']
    
    X_test = test[[f'lag_{i}' for i in range(1, 8)]]
    y_test = test['ProductionUnits']
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    pred = model.predict(X_test)
    
    error = mape(y_test, pred)
    
    results.append((plant, error))

# Print results
for plant, error in results:
    print(f"{plant} → MAPE: {error:.2f}%")