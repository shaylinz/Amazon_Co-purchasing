import pandas as pd
import json
import matplotlib.pyplot as plt

def load_data_from_json(file_name):
    data = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                entry = json.loads(line)
                entry['num_similar'] = entry.get('similar', {}).get('count', 0)
                data.append(entry)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line}, error: {e}")
    return pd.DataFrame(data)

file_name = 'amazon-meta.json'
df = load_data_from_json(file_name)

# Sort, compute rolling means
df_sorted = df.sort_values(by='salesrank', ascending=True)
window_size = 50
df_sorted['smooth_sales_rank'] = df_sorted['salesrank'].rolling(window=window_size, min_periods=1).mean()
df_sorted['smooth_num_similar'] = df_sorted['num_similar'].rolling(window=window_size, min_periods=1).mean()

# Calculate and display the Pearson correlation coefficient
correlation_smoothed = df_sorted['smooth_sales_rank'].corr(df_sorted['smooth_num_similar'])
print(f"Correlation between smoothed sales rank and smoothed number of similar items: {correlation_smoothed}")

# Plot using plt.plot for a line plot
plt.figure(figsize=(10, 6))
plt.plot(df_sorted['smooth_sales_rank'], df_sorted['smooth_num_similar'], 'r-', alpha=0.5)  # 'r-' for a red line
plt.title('Smoothed Number of Similar Items vs. Smoothed Sales Rank')
plt.xlabel('Smoothed Sales Rank')
plt.ylabel('Smoothed Number of Similar Items')
plt.show()
