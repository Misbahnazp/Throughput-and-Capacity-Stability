import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, classification_report

file_path = "THROUGHPUT & CAPACITY STABILITY (2).xlsx"
df = pd.read_excel(file_path)

print("Data Loaded Successfully\n")
print(df.head())

df['Timestamp'] = pd.to_datetime(df['Timestamp'])

df['Hour'] = df['Timestamp'].dt.hour

df['P10'] = df.groupby(['Plant', 'Hour'])['ProductionUnits'].transform(
    lambda x: np.percentile(x, 10)
)

df['LowOutputEvent'] = (df['ProductionUnits'] < df['P10']).astype(int)

print("\n Target Variable Created")
print(df[['ProductionUnits', 'P10', 'LowOutputEvent']].head())

sensor_cols = [col for col in df.columns if 'Sensor' in col]

features = sensor_cols + ['EnergyConsumption']

X = df[features]
y = df['LowOutputEvent']

X = X.fillna(X.mean())

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced'
)

model.fit(X_train, y_train)

print("\nModel Training Completed")

y_pred = model.predict(X_test)

f1 = f1_score(y_test, y_pred)

print("\n F1 Score:", round(f1, 4))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

importance = pd.Series(model.feature_importances_, index=X.columns)

print("\nFeature Importance:\n")
print(importance.sort_values(ascending=False))

