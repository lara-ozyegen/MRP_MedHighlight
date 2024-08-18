"""
This script converts the PHEE dataset to binary labels and forms the PHEE-2 dataset.
"""
import pandas as pd
import ast

def map_to_binary(labels):
    binary_labels = ['O' if label == 'O' else 'I' for label in labels]
    return binary_labels

# read csv file

file_path = 'data/processed/phee/fold0/test.csv'
df = pd.read_csv(file_path)
df['tag'] = df['tag'].apply(ast.literal_eval)
print(df.head())
df['tag'] = df['tag'].apply(map_to_binary)
df

# save to csv
df.to_csv('data/processed/phee/fold0/binary_test.csv', index=False)


