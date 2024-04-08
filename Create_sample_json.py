import pandas as pd
import json
import random

def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0

def title_similarity(title1, title2):
    words1 = set(title1.split())
    words2 = set(title2.split())
    return jaccard_similarity(words1, words2)

def category_similarity(categories1, categories2):
    set1 = set(categories1)
    set2 = set(categories2)
    return jaccard_similarity(set1, set2)

def load_data(json_file):
    products = []
    with open(json_file, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                product = json.loads(line)
                products.append(product)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return products

# def extract_categories(category_path):
#     # Assuming categories are separated by '|', and the actual category is in brackets []
#     return [part[part.find("[")+1:part.find("]")] for part in category_path if '[' in part and ']' in part]

def generate_co_purchased_pairs(products):
    co_purchased_pairs = []
    asin_to_product = {product['ASIN']: product for product in products}
    count=0

    for product in products:
        if(len(co_purchased_pairs)<5000):
            asin = product['ASIN']
            if 'similar' in product and 'items' in product['similar']:
                similar_asins = product['similar']['items']
                for similar_asin in similar_asins:
                    if similar_asin in asin_to_product:
                        similar_product = asin_to_product[similar_asin]
                        pair = {
                            'title_sim': title_similarity(product.get('title', ''), similar_product.get('title', '')),
                            'cat_sim': category_similarity(product.get('categories', []),similar_product.get('categories', [])),
                            'avg_rating_1': product.get('avg_rating', 0),
                            'avg_rating_2': similar_product.get('avg_rating', 0),
                            'sales_rank_1': product.get('salesrank', None),
                            'sales_rank_2': similar_product.get('salesrank', None),
                            'co_purchased': 1
                        }
                        co_purchased_pairs.append(pair)
                        count+=1
                        print(count)
        else:
            break
    return co_purchased_pairs



def generate_non_co_purchased_pairs(products, co_purchased_pairs, num_pairs=5000):
    non_co_purchased_pairs = []
    asin_list = [product['ASIN'] for product in products]
    attempts = 0

    while len(non_co_purchased_pairs) < num_pairs and attempts < 10 * num_pairs:
        # Randomly select two products
        asin1, asin2 = random.sample(asin_list, 2)
        product1 = next((p for p in products if p['ASIN'] == asin1), None)
        product2 = next((p for p in products if p['ASIN'] == asin2), None)

        if not product1 or not product2:
            continue  # Skip if product not found

        # Check if not co-purchased
        if asin2 not in product1.get('similar', {}).get('items', []) and asin1 not in product2.get('similar', {}).get('items', []):
            pair = {
                'title_sim': title_similarity(product1.get('title', ''), product2.get('title', '')),
                'cat_sim': category_similarity(product1.get('categories', []), product2.get('categories', [])),
                'avg_rating_1': product1.get('avg_rating', 0),
                'avg_rating_2': product2.get('avg_rating', 0),
                'sales_rank_1': product1.get('salesrank', None),
                'sales_rank_2': product2.get('salesrank', None),
                'co_purchased': 0
            }
            non_co_purchased_pairs.append(pair)
        
        attempts += 1
        print(attempts)

    return non_co_purchased_pairs

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Load products from the JSON file
products = load_data('amazon-meta.json')

# Generate co-purchased pairs
co_purchased_pairs = generate_co_purchased_pairs(products)

# Generate non co-purchased pairs
non_co_purchased_pairs = generate_non_co_purchased_pairs(products, co_purchased_pairs, 5000)

# Combine both lists
all_pairs = co_purchased_pairs + non_co_purchased_pairs

# Save all pairs to a new JSON file
save_to_json(all_pairs, 'all_product_pairs.json')

print(f"Saved {len(all_pairs)} product pairs to 'all_product_pairs.json'")