import pandas as pd
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
import json

# Function to load JSON data into a DataFrame
def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Load the data
df = load_data('all_product_pairs.json')

# Handle missing values - Dropping rows with any missing values in specified columns
df = df.dropna(subset=["title_sim", "cat_sim", "avg_rating_1", "avg_rating_2", "sales_rank_1", "sales_rank_2", "co_purchased"])

# Features and target variable
X = df[["title_sim", "cat_sim", "avg_rating_1", "avg_rating_2", "sales_rank_1", "sales_rank_2"]]
y = df['co_purchased']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# AdaBoost Classifier with the SAMME algorithm
ada_boost_model = AdaBoostClassifier(n_estimators=50, random_state=42, algorithm='SAMME')

# Cross-validation
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
scores = cross_val_score(ada_boost_model, X_scaled, y, cv=cv, scoring='accuracy')

# Print the accuracy
print("Accuracy for each fold: ", scores)
print("Average cross-validation score: {:.4f}".format(scores.mean()))