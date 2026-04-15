import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, classification_report

# 2. LOAD DATASET
file_path = "THROUGHPUT & CAPACITY STABILITY (2).xlsx"
df = pd.read_excel(file_path)

print("✅ Data Loaded Successfully\n")
print(df.head())

# 3. DATA PREPROCESSING
# Convert Timestamp column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Extract hour from timestamp
df['Hour'] = df['Timestamp'].dt.hour

# 4. CREATE TARGET VARIABLE
# Calculate 10th percentile per Plant-Hour
df['P10'] = df.groupby(['Plant', 'Hour'])['ProductionUnits'].transform(
    lambda x: np.percentile(x, 10)
)

# Create LowOutputEvent (1 = Low Output, 0 = Normal)
df['LowOutputEvent'] = (df['ProductionUnits'] < df['P10']).astype(int)

print("\n✅ Target Variable Created")
print(df[['ProductionUnits', 'P10', 'LowOutputEvent']].head())

# 5. FEATURE SELECTION
# Select sensor columns automatically
sensor_cols = [col for col in df.columns if 'Sensor' in col]

# Final features
features = sensor_cols + ['EnergyConsumption']

X = df[features]
y = df['LowOutputEvent']

# 6. HANDLE MISSING VALUES
X = X.fillna(X.mean())

# 7. TRAIN-TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 8. TRAIN MODEL
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced'
)

model.fit(X_train, y_train)

print("\n✅ Model Training Completed")

# 9. MAKE PREDICTIONS
y_pred = model.predict(X_test)

# 10. EVALUATE MODEL
f1 = f1_score(y_test, y_pred)

print("\n🎯 F1 Score:", round(f1, 4))

print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# 11. FEATURE IMPORTANCEs
importance = pd.Series(model.feature_importances_, index=X.columns)

print("\n🔥 Feature Importance:\n")
print(importance.sort_values(ascending=False))

