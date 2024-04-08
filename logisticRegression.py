import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import json

# Adjust the load_data function for a typical JSON structure
def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)  # Load the entire file as a JSON object/array
    return pd.DataFrame(data)

# Load the data
df = load_data('all_product_pairs.json')

# Drop rows with missing values for simplicity (consider imputation as a better alternative)
df = df.dropna(subset=["title_sim", "cat_sim", "avg_rating_1", "avg_rating_2", "sales_rank_1", "sales_rank_2", "co_purchased"])

# Features and target variable
X = df[["title_sim", "cat_sim", "avg_rating_1", "avg_rating_2", "sales_rank_1", "sales_rank_2"]]
y = df['co_purchased']

# Scaling features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Model training and evaluation using cross-validation
logistic_model = LogisticRegression(max_iter=1000)  # Increase max_iter if convergence warning

# Using StratifiedKFold for cross-validation to maintain the proportion of the target class
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
scores = cross_val_score(logistic_model, X_scaled, y, cv=cv, scoring='accuracy')

# Print the accuracy for each fold and the average accuracy
print("Accuracy for each fold: ", scores)
print("Average cross-validation score: {:.4f}".format(scores.mean()))
