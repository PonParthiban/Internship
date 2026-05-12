# ============================================================
#  ML FUNDAMENTALS — Full Pipeline Tutorial
#  Tools: NumPy · Pandas · Scikit-learn
#  Example dataset: Predicting house prices
# ============================================================

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from sklearn.pipeline import Pipeline


# ============================================================
# STEP 0 — Create a sample raw dataset (simulating messy data)
# ============================================================

np.random.seed(42)
n = 200

raw_data = pd.DataFrame({
    "size_sqft":    np.random.randint(500, 3000, n).astype(float),
    "bedrooms":     np.random.choice([1, 2, 3, 4, 5, np.nan], n),
    "age_years":    np.random.randint(0, 50, n).astype(float),
    "location":     np.random.choice(["Chennai", "Mumbai", "Delhi", np.nan], n),
    "price_lakhs":  np.random.randint(20, 300, n).astype(float),
})

# Inject some messiness
raw_data.loc[5,  "size_sqft"]   = 999999   # outlier
raw_data.loc[10, "price_lakhs"] = np.nan   # missing target
raw_data.loc[15, "age_years"]   = np.nan   # missing value
raw_data = pd.concat([raw_data, raw_data.iloc[[3, 7]]], ignore_index=True)  # duplicates

print("=" * 60)
print("RAW DATA — first 5 rows")
print("=" * 60)
print(raw_data.head())
print(f"\nShape: {raw_data.shape}")
print(f"Missing values:\n{raw_data.isnull().sum()}")


# ============================================================
# STEP 1 — DATA CLEANING  (pandas + numpy)
# ============================================================
print("\n" + "=" * 60)
print("STEP 1 — DATA CLEANING")
print("=" * 60)

df = raw_data.copy()

# 1a. Remove duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows → {len(df)} rows remain")

# 1b. Drop rows where the TARGET is missing (can't train without it)
df = df.dropna(subset=["price_lakhs"])
print(f"After dropping missing targets → {len(df)} rows")

# 1c. Handle outliers using IQR (Interquartile Range) method
#     Any value beyond 1.5 × IQR from Q1/Q3 is capped (clipped)
for col in ["size_sqft", "age_years"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = ((df[col] < lower) | (df[col] > upper)).sum()
    df[col] = df[col].clip(lower, upper)
    print(f"  '{col}': clipped {outliers} outlier(s) → range [{lower:.0f}, {upper:.0f}]")

print(f"\nAfter cleaning → shape: {df.shape}")
print(f"Remaining missing values:\n{df.isnull().sum()}")


# ============================================================
# STEP 2 — FEATURE EXTRACTION / HANDLING MISSING VALUES
#           (pandas + sklearn SimpleImputer)
# ============================================================
print("\n" + "=" * 60)
print("STEP 2 — FEATURE EXTRACTION & IMPUTATION")
print("=" * 60)

# Separate numeric and categorical columns
numeric_cols     = ["size_sqft", "bedrooms", "age_years"]
categorical_cols = ["location"]

# 2a. Impute missing NUMERIC values with the MEDIAN
#     (median is better than mean when data has skew)
num_imputer = SimpleImputer(strategy="median")
df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])
print(f"Numeric medians used for imputation: "
      f"{dict(zip(numeric_cols, num_imputer.statistics_))}")

# 2b. Impute missing CATEGORICAL values with the MOST FREQUENT value
cat_imputer = SimpleImputer(strategy="most_frequent")
df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])
print(f"Categorical fill: {cat_imputer.statistics_}")

print(f"\nMissing values after imputation:\n{df.isnull().sum()}")


# ============================================================
# STEP 3 — FEATURE ENGINEERING  (pandas + numpy)
# ============================================================
print("\n" + "=" * 60)
print("STEP 3 — FEATURE ENGINEERING")
print("=" * 60)

# 3a. Create a new feature: price per square foot
#     (domain knowledge: this ratio is very predictive)
df["price_per_sqft"] = df["price_lakhs"] / df["size_sqft"]

# 3b. Age category bins — age as a raw number isn't as useful
#     as grouping into "new / mid-age / old"
df["age_group"] = pd.cut(
    df["age_years"],
    bins=[0, 10, 30, 50],
    labels=["new", "mid", "old"]
)

# 3c. Room density: bedrooms relative to house size
df["room_density"] = df["bedrooms"] / df["size_sqft"] * 1000

# 3d. One-Hot Encode the 'location' categorical column
#     "Chennai" → [1, 0, 0], "Mumbai" → [0, 1, 0], etc.
df = pd.get_dummies(df, columns=["location"], drop_first=True)

# 3e. Encode 'age_group' (ordinal)
le = LabelEncoder()
df["age_group_encoded"] = le.fit_transform(df["age_group"].astype(str))

print("New features created:")
print("  price_per_sqft, age_group, room_density, location dummies, age_group_encoded")
print(f"\nDataframe columns now:\n{list(df.columns)}")
print(f"\nSample rows:\n{df.head(3)}")


# ============================================================
# STEP 4 — TRAIN / TEST SPLIT  (sklearn)
# ============================================================
print("\n" + "=" * 60)
print("STEP 4 — TRAIN / TEST SPLIT")
print("=" * 60)

# Define features (X) and target (y)
# Drop the target and intermediate columns we don't feed to the model
drop_cols = ["price_lakhs", "price_per_sqft", "age_group"]
feature_cols = [c for c in df.columns if c not in drop_cols]

X = df[feature_cols]
y = df["price_lakhs"]

print(f"Features (X): {list(X.columns)}")
print(f"Target  (y): price_lakhs")

# 80% train, 20% test — random_state ensures reproducibility
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set : {X_train.shape[0]} rows")
print(f"Test set     : {X_test.shape[0]} rows")


# ============================================================
# STEP 5 — NORMALIZATION / SCALING  (sklearn StandardScaler)
# ============================================================
print("\n" + "=" * 60)
print("STEP 5 — SCALING / NORMALIZATION")
print("=" * 60)

# StandardScaler: transforms each feature to mean=0, std=1
# IMPORTANT: fit ONLY on training data, then transform both
#            (leaking test stats into training = data leakage!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)        # no re-fitting here!

print("Scaling applied: mean=0, std=1 per feature")
print(f"  Feature means (train): {scaler.mean_.round(2)}")
print(f"  Feature stds  (train): {scaler.scale_.round(2)}")
print(f"\nBefore scaling — size_sqft range: {X_train['size_sqft'].min():.0f} to {X_train['size_sqft'].max():.0f}")
print(f"After  scaling — size_sqft range: {X_train_scaled[:, 0].min():.2f} to {X_train_scaled[:, 0].max():.2f}")


# ============================================================
# STEP 6 — MODEL TRAINING  (sklearn)
# ============================================================
print("\n" + "=" * 60)
print("STEP 6 — MODEL TRAINING")
print("=" * 60)

# --- Model A: Linear Regression (simple, interpretable) ---
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)
print("Linear Regression trained.")
print(f"  Coefficients (first 4): {lr_model.coef_[:4].round(2)}")
print(f"  Intercept             : {lr_model.intercept_:.2f}")

# --- Model B: Random Forest (more powerful, handles non-linearity) ---
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)
print("\nRandom Forest trained (100 decision trees).")

# Feature importance — which features matter most?
importances = pd.Series(
    rf_model.feature_importances_,
    index=feature_cols
).sort_values(ascending=False)
print(f"\nTop 4 most important features:\n{importances.head(4).round(3)}")


# ============================================================
# STEP 7 — EVALUATION  (sklearn metrics)
# ============================================================
print("\n" + "=" * 60)
print("STEP 7 — MODEL EVALUATION")
print("=" * 60)

for name, model in [("Linear Regression", lr_model), ("Random Forest", rf_model)]:
    y_pred = model.predict(X_test_scaled)
    rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
    r2     = r2_score(y_test, y_pred)
    print(f"\n{name}:")
    print(f"  RMSE (error in lakhs) : {rmse:.2f}")
    print(f"  R²   (variance explained): {r2:.3f}  (1.0 = perfect)")

# Cross-validation: more reliable than a single train/test split
cv_scores = cross_val_score(rf_model, X_train_scaled, y_train,
                             cv=5, scoring="r2")
print(f"\nRandom Forest — 5-fold Cross Validation R² scores:")
print(f"  {cv_scores.round(3)}")
print(f"  Mean: {cv_scores.mean():.3f}  |  Std: {cv_scores.std():.3f}")


# ============================================================
# STEP 8 — SKLEARN PIPELINE  (production-ready pattern)
# ============================================================
print("\n" + "=" * 60)
print("STEP 8 — SKLEARN PIPELINE (clean, production pattern)")
print("=" * 60)

# A Pipeline chains steps so you can't accidentally
# forget to scale test data or fit on wrong data
pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler",  StandardScaler()),
    ("model",   RandomForestRegressor(n_estimators=50, random_state=42)),
])

# Use only numeric columns for this demo pipeline
X_num = df[["size_sqft", "bedrooms", "age_years", "room_density", "age_group_encoded"]]
y_all = df["price_lakhs"]

X_tr, X_te, y_tr, y_te = train_test_split(X_num, y_all, test_size=0.2, random_state=42)
pipe.fit(X_tr, y_tr)
pipe_preds = pipe.predict(X_te)
pipe_r2 = r2_score(y_te, pipe_preds)

print("Pipeline steps: Imputer → Scaler → RandomForest")
print(f"Pipeline R²: {pipe_r2:.3f}")
print("\nAll steps done in one .fit() call — clean and safe!")


# ============================================================
# QUICK REFERENCE CHEATSHEET
# ============================================================
print("\n" + "=" * 60)
print("QUICK REFERENCE CHEATSHEET")
print("=" * 60)
cheatsheet = """
TASK                         CODE
----                         ----
Load CSV                     pd.read_csv("file.csv")
Check missing                df.isnull().sum()
Fill missing (median)        df.fillna(df.median())
Impute (sklearn)             SimpleImputer(strategy="median").fit_transform(X)
Remove duplicates            df.drop_duplicates()
Clip outliers                df[col].clip(lower, upper)
One-hot encode               pd.get_dummies(df, columns=["col"])
Label encode                 LabelEncoder().fit_transform(df["col"])
Train/test split             train_test_split(X, y, test_size=0.2)
Scale features               StandardScaler().fit_transform(X_train)
Train model                  model.fit(X_train, y_train)
Predict                      model.predict(X_test)
RMSE                         np.sqrt(mean_squared_error(y_test, y_pred))
R² score                     r2_score(y_test, y_pred)
Cross-validate               cross_val_score(model, X, y, cv=5)
Feature importance           model.feature_importances_
Full pipeline                Pipeline([("scaler", ...), ("model", ...)])
"""
print(cheatsheet)
