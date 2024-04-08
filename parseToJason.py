import gzip
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from datetime import datetime
import json




def parse_amazon_metadata_to_json(input_file_path, output_file_path):
    with gzip.open(input_file_path, 'rt', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        product = {}
        reviews = []
        collecting_reviews = False

        for line in infile:
            line = line.strip()
            if line.startswith("Id:"):
                # If we encounter a new product, save the previous one first
                if product:
                    product['reviews'] = reviews
                    json.dump(product, outfile)
                    outfile.write('\n')
                    reviews = []
                product = {'Id': line.split()[1]}
            elif line.startswith("ASIN:"):
                product['ASIN'] = line.split()[1]
            elif line.startswith("title:"):
                product['title'] = line[len("title:"):].strip()
            elif line.startswith("group:"):
                product['group'] = line.split(":")[1].strip()
            elif line.startswith("salesrank:"):
                product['salesrank'] = int(line.split(":")[1].strip())
            elif line.startswith("similar:"):
                similar_items = line.split()
                if len(similar_items) >= 3:  # Ensure there's at least one similar item
                    product['similar'] = {'count': int(similar_items[1]), 'items': similar_items[2:]}
                else:
                    product['similar'] = {'count': 0, 'items': []}  # No similar items
            elif line.startswith("categories:"):
                product['categories'] = []
                collecting_reviews = False  # Stop collecting reviews if we were
            elif line.startswith("|"):
                product['categories'].append(line.strip("|").strip())
            elif line.startswith("reviews:"):
                collecting_reviews = True
                parts = line.split()
                product['avg_rating'] = float(parts[-1])  # The average rating is the last part of the line
            elif collecting_reviews and line.startswith("20"):
                # Assuming review lines start with a date
                parts = line.split()
                review = {
                    'date': parts[0],
                    'customer': parts[2],
                    'rating': int(parts[4]),
                    'votes': int(parts[6]),
                    'helpful': int(parts[8])
                }
                reviews.append(review)

        # Don't forget the last product
        if product:
            product['reviews'] = reviews
            json.dump(product, outfile)

parse_amazon_metadata_to_json('amazon-meta.txt.gz', 'amazon-meta.json')
