import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score

# Load dataset
file_path = "collected_alpha_power_results.csv"
data = pd.read_csv(file_path)

# Ensure "Dataset No." is treated as a string
data["Dataset No."] = data["Dataset No."].astype(str)

# Handle missing values (fill with column mean)
imputer = SimpleImputer(strategy="mean")
X = data.iloc[:, :-2]  # Select only EEG features (excluding 'Stress' and 'Dataset No.')
X = imputer.fit_transform(X)

# Extract labels and groups
y = data["Stress"]
groups = data["Dataset No."]

# Normalize EEG features for better performance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into train/test sets while keeping subjects together
group_kfold = GroupKFold(n_splits=5)
train_idx, test_idx = next(group_kfold.split(X_scaled, y, groups))

print (train_idx)
print (test_idx)

X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]




# Train Random Forest model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict on test set
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.2f}")

# Cross-validation
cv_scores = cross_val_score(clf, X_scaled, y, cv=group_kfold, groups=groups, scoring="accuracy")
print(f"Cross-Validation Accuracy: {np.mean(cv_scores):.2f} ± {np.std(cv_scores):.2f}")

