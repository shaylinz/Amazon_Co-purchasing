import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

# Load your JSON data into a DataFrame
def load_json_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data)

filename = 'all_product_pairs.json'
df = load_json_file(filename)


# Creating bins for title similarity
df['title_sim_bin'] = pd.cut(df['title_sim'], bins=10, labels=range(10))
df['title_sim_bin'] = df['title_sim_bin'].astype(int)  # Convert bin labels to integer for easier handling

# Calculating the mean co-purchasing rate for each title similarity bin
df_grouped = df.groupby('title_sim_bin')['co_purchased'].mean().reset_index()
df_grouped['title_sim_bin'] = (df_grouped['title_sim_bin'] - df_grouped['title_sim_bin'].min()) / (df_grouped['title_sim_bin'].max() - df_grouped['title_sim_bin'].min())  # Normalize bin numbers

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df_grouped['title_sim_bin'], df_grouped['co_purchased'], marker='o', linestyle='-', color='b')
plt.xlabel('Normalized Title Similarity Bin')
plt.ylabel('Average Co-Purchasing Rate')
plt.title('Co-Purchasing Rate vs. Normalized Title Similarity Bin')
plt.grid(True)
plt.show()

# Correlation calculation and output as before
correlation_title = np.corrcoef(df['title_sim_bin'], df['co_purchased'])[0, 1]
print(f"Correlation between title similarity bins and co-purchasing rate: {correlation_title}")
