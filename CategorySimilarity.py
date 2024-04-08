import gzip
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

def parse_data(file_name):
    products = {}
    with gzip.open(file_name, 'rt', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Id"):
                current_id = line.split()[1]
                products[current_id] = {"title": "", "group": "", "similar": set(), "categories": []}
            elif line.startswith("group"):
                products[current_id]["group"] = line.split(":")[1].strip()
            elif line.startswith("title"):
                products[current_id]["title"] = line.split(":", 1)[1].strip().lower()
            elif line.startswith("similar"):
                similar_ids = line.split()[2:]
                products[current_id]["similar"] = set(similar_ids)
            elif line.startswith("categories"):
                # Assuming categories are listed one per line after "categories" entry
                products[current_id]["categories"] = []
                categories_line = next(file).strip()
                while categories_line.startswith("|"):
                    products[current_id]["categories"].append(categories_line.strip("|").split("|"))
                    categories_line = next(file).strip()
    return products

def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0

def category_similarity(categories1, categories2):
    # Simple similarity check: 1 if they share any category, 0 otherwise
    set1 = set(tuple(cat) for cat in categories1)
    set2 = set(tuple(cat) for cat in categories2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0
 

# Assuming you've parsed your data into the `products` dictionary
file_name = 'amazon-meta.txt.gz'
products = parse_data(file_name)

# Select a random sample of products
product_ids = list(products.keys())
sample_ids = random.sample(product_ids, 3000)  # Adjust the sample size as needed

# Calculate co-purchasing rate for pairs in the sample
pairwise_data = []

for i in range(len(sample_ids)):
    for j in range(i + 1, len(sample_ids)):
        product_a = products[sample_ids[i]]
        product_b = products[sample_ids[j]]
        co_purchase_rate = jaccard_similarity(product_a['similar'], product_b['similar'])
        pairwise_data.append((sample_ids[i], sample_ids[j], co_purchase_rate))

# Filter out pairs with zero co-purchasing rate and limit to less than 10%
non_zero_pairs = [pair for pair in pairwise_data if pair[2] > 0]
max_zero_pairs = len(non_zero_pairs) // 9  # Allow up to 10% zero rates
zero_pairs = [pair for pair in pairwise_data if pair[2] == 0][:max_zero_pairs]
filtered_pairs = non_zero_pairs + zero_pairs

# Calculate title similarities only for the filtered pairs
filtered_cat_similarities = []
filtered_co_purchasing_rates = []

for pair in filtered_pairs:
    product_a = products[pair[0]]
    product_b = products[pair[1]]
    if product_a['title'] and product_b['title']:  # Ensure both titles are non-empty
        cat_sim = category_similarity(product_a['title'], product_b['title'])
        filtered_cat_similarities.append(cat_sim)
        filtered_co_purchasing_rates.append(pair[2])

# Create the DataFrame with the filtered data
data = {
    'cat_similarity': filtered_cat_similarities,
    'co_purchasing_rate': filtered_co_purchasing_rates
}
df_filtered = pd.DataFrame(data)

# Sort, normalize, and plot as before
df_sorted = df_filtered.sort_values(by='cat_similarity', ascending=True)

window_size = 50  # The window size can be adjusted as needed
df_sorted['smooth_co_purchasing_rate'] = df_sorted['co_purchasing_rate'].rolling(window=window_size, min_periods=1).mean()

# Normalize the values
df_sorted['cat_similarity'] = (df_sorted['cat_similarity'] - df_sorted['cat_similarity'].min()) / (df_sorted['cat_similarity'].max() - df_sorted['cat_similarity'].min())
df_sorted['smooth_co_purchasing_rate'] = (df_sorted['smooth_co_purchasing_rate'] - df_sorted['smooth_co_purchasing_rate'].min()) / (df_sorted['smooth_co_purchasing_rate'].max() - df_sorted['smooth_co_purchasing_rate'].min())

correlation = df_filtered['cat_similarity'].corr(df_filtered['smooth_co_purchasing_rate'])
print(f"Pearson's correlation coefficient: {correlation}")


# # Plotting
# plt.figure(figsize=(10, 6))
# plt.scatter(df_sorted['cat_similarity'], df_sorted['smooth_co_purchasing_rate'])
# plt.xlabel('Title Similarity')
# plt.ylabel('Smoothed Co-Purchasing Rate')
# plt.title('Co-Purchasing Rate vs. cat_similarity')
# plt.show()
