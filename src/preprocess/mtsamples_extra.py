"""
This script reads the mtsamples.csv file and processes the data to be used for unsupervised learning.
"""

import pandas as pd
import pandas as pd
from docx import Document
import string
import re

# read csv
df = pd.read_csv("data/raw/mtsamples.csv")
df= df.drop('Unnamed: 0', axis=1)
df = df["description"].sample(frac=1, random_state=42).reset_index(drop=True)

# read csv
df = pd.read_csv("data/raw/mtsamples.csv")
df= df.drop('Unnamed: 0', axis=1)
df = df["description"].sample(frac=1, random_state=42).reset_index(drop=True)

# Write the description to a TXT file
description_file_path = "data/processed/mtsamples2/unsupervised_mtsamples.txt"
with open(description_file_path, "w") as txt_file:
    for description in df:
        txt_file.write(description + '\n')


# Create a new Word document
doc = Document()
# Add each description to the Word document
for index, row in df[:200].iterrows():
    doc.add_paragraph(f"{row['description']}\n")



# Define the punctuation to modify, excluding hyphens
modified_punctuation = string.punctuation.replace('-', '')

# Function to add space around punctuation
def add_space_around_punctuation(text):
    for punct in modified_punctuation:
        text = text.replace(punct, f' {punct} ')
    return re.sub(r'\s{2,}', ' ', text)  # Replace multiple spaces with a single space

# Apply the function to each description
df['description'] = df['description'].apply(add_space_around_punctuation)






