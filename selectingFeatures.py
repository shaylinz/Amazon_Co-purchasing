import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import json

# Function to load JSON data from a file
def load_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

filename = 'all_product_pairs.json'
data_list = load_json_file(filename)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data_list)

# Remove rows with NaN values from the DataFrame
df_clean = df.dropna()


# Now that df is cleaned from NaN values, proceed with preparing your feature matrices and target vector
y_clean = df_clean['co_purchased']

X1_clean = df_clean[['sales_rank_1', 'sales_rank_2']]
X2_clean = df_clean[['sales_rank_1', 'sales_rank_2', 'avg_rating_1', 'avg_rating_2']]
X3_clean = df_clean[['sales_rank_1', 'sales_rank_2', 'avg_rating_1', 'avg_rating_2', 'cat_sim']]
X4_clean = df_clean[['sales_rank_1', 'sales_rank_2', 'avg_rating_1', 'avg_rating_2', 'cat_sim', 'title_sim']]

# Model training and evaluation using cross-validation
logistic_model = LogisticRegression(max_iter=1000)  # Increased max_iter for convergence

# Using StratifiedKFold for cross-validation to maintain the proportion of the target class
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Perform cross-validation using the cleaned datasets
scores1 = cross_val_score(logistic_model, X1_clean, y_clean, cv=cv, scoring='accuracy')
scores2 = cross_val_score(logistic_model, X2_clean, y_clean, cv=cv, scoring='accuracy')
scores3 = cross_val_score(logistic_model, X3_clean, y_clean, cv=cv, scoring='accuracy')
scores4 = cross_val_score(logistic_model, X4_clean, y_clean, cv=cv, scoring='accuracy')

# Print the accuracy for each fold and the average accuracy
print("Average cross-validation score1: {:.8f}".format(scores1.mean()))
print("Average cross-validation score2: {:.8f}".format(scores2.mean()))
print("Average cross-validation score3: {:.8f}".format(scores3.mean()))
print("Average cross-validation score4: {:.8f}".format(scores4.mean()))
