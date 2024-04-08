import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

# Function to load JSON data into a DataFrame
def load_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data)

# Load data
filename = 'all_product_pairs.json'  # Adjust the filename to your JSON file's path
df = load_json_file(filename)
df = df.dropna()  # Drop rows with missing values to ensure clean data for analysis

# Create bins for category similarity for analysis
df['cat_sim_bin'] = pd.cut(df['cat_sim'], bins=10, labels=False)

# Calculate co-purchasing rate within each category similarity bin
co_purchasing_rate_by_cat_sim = df.groupby('cat_sim_bin')['co_purchased'].mean()

# Print the co-purchasing rates for each bin
print(co_purchasing_rate_by_cat_sim)

# Calculate and print the Pearson correlation coefficient between category similarity bins and co-purchasing rate
correlation = np.corrcoef(df['cat_sim_bin'], df['co_purchased'])[0, 1]
print(f"Correlation between category similarity bins and co-purchasing rate: {correlation}")

# Plotting the co-purchasing rate by category similarity bin
co_purchasing_rate_df = co_purchasing_rate_by_cat_sim.reset_index()  # Convert Series to DataFrame for plotting

plt.figure(figsize=(10, 6))
plt.plot(co_purchasing_rate_df['cat_sim_bin'], co_purchasing_rate_df['co_purchased'], marker='o', linestyle='-', color='b')
plt.title('Co-Purchasing Rate by Category Similarity Bin')
plt.xlabel('Category Similarity Bin')
plt.ylabel('Average Co-Purchasing Rate')
plt.grid(True)
plt.show()
