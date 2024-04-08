import pandas as pd
import json
import matplotlib.pyplot as plt

def load_data_from_json(file_name):
    data = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                entry = json.loads(line)
                # Directly use the 'count' from the 'similar' section for 'num_similar'
                entry['num_similar'] = entry.get('similar', {}).get('count', 0)
                data.append(entry)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line}, error: {e}")
    return pd.DataFrame(data)

file_name = 'amazon-meta.json'  # Ensure this is the correct path to your JSON file
df = load_data_from_json(file_name)

# Now that 'num_similar' is correctly captured, proceed with your analysis
df_sorted = df.sort_values(by='avg_rating', ascending=True)
window_size = 50
df_sorted['smooth_avg_rating'] = df_sorted['avg_rating'].rolling(window=window_size, min_periods=1).mean()
df_sorted['smooth_num_similar'] = df_sorted['num_similar'].rolling(window=window_size, min_periods=1).mean()

# Calculate and print the Pearson correlation coefficient for the smoothed values
correlation_smoothed = df_sorted['smooth_avg_rating'].corr(df_sorted['smooth_num_similar'])
print(f"Correlation between avg_rating and smoothed number of similar items: {correlation_smoothed}")

plt.figure(figsize=(10, 6))
plt.scatter(df['avg_rating'], df['num_similar'], alpha=0.5)
plt.title('Number of Similar Items vs. Average Rating')
plt.xlabel('Number of Similar Items')
plt.ylabel('Average Rating')
plt.show()
