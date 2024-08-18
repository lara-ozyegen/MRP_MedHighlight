"""
This script preprocesses the raw phee dataset. 
It tokenizes the sentences and labels them as Problem, Test and Treatment using clinical BERT model. 
The results are saved in csv files.
These results are used to set the 'Test' tag in the PHEE-6 dataset.
"""

import torch
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import AutoTokenizer, AutoModelForTokenClassification
import string

'''
Get the raw phee dataset. Give it to clinical BERT model (labels the sentences as Problem, Test and Treatment). Save the results in csv files. 
Sentence_ID
Org_Sentence: original sentence (the version in phee)
Org_Tag: original tag (the version in phee)
Sentence: tokenized sentence (with bert tokenizer)
Tag: tags that come from clinical BERT model
'''
files = ['train', 'dev', 'test']
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("samrawal/bert-base-uncased_clinical-ner")
model = AutoModelForTokenClassification.from_pretrained("samrawal/bert-base-uncased_clinical-ner")
model.to(device)

def process_sentence(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, add_special_tokens=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)[0]
    labels = [model.config.id2label[label_id.item()] for label_id in predictions[1:-1].cpu()]  # Exclude [CLS], [SEP]
    united_labels = []
    united_tokens = []
    # ignore words that are split into subwords
    
    for token, label in zip(tokenizer.tokenize(sentence), labels):
        if token.startswith('##'):
            united_tokens[-1] = united_tokens[-1] + token[2:]
            continue
        united_tokens.append(token)
        united_labels.append(label)

    return united_tokens, united_labels

def drop_duplicates(df):
    # Initial number of samples
    initial_count = len(df)

    # Identify duplicates for 'Sentence' and 'Tag' columns
    duplicates_both = df.duplicated(subset=['Org_Sentence', 'Org_Tag'], keep=False)

    # Identify duplicates only based on 'Sentence'
    duplicates_sentence = df.duplicated(subset=['Org_Sentence'], keep=False)

    # Filter out the rows where 'Sentence' is duplicated but 'Tag' is not
    to_drop =df[duplicates_sentence & ~duplicates_both]

    # Count the number of rows to be dropped
    drop_count = len(to_drop)

    # Drop the identified rows
    df = df.drop(to_drop.index)

    # Now, drop duplicate rows based on both 'Sentence' and 'Tag'
    df = df.drop_duplicates(subset=['Org_Sentence', 'Org_Tag'])

    # Calculate the number of samples removed
    samples_removed = initial_count - len(df)

    # Report the numbers
    print(f"Initial count of samples: {initial_count}")
    print(f"Number of ambiguous samples (duplicated 'Org_Sentence' but not 'Org_Tag'): {drop_count}")
    print(f"Total samples removed: {samples_removed}")

    return df


def preprocess(file_name):
    # Reading the file and creating a DataFrame
    with open(f'data/raw/phee/ace/{file_name}.txt', 'r') as file:
        lines = file.readlines()

    words, tags, sentence_ids = [], [], []
    sentence_id = 0

    for line in lines:
        if line.strip() == '':  # Check for empty line indicating end of sentence
            sentence_id += 1
        else:
            word, tag = line.strip().split()
            words.append(word)
            tags.append(tag)
            sentence_ids.append(sentence_id)

    # Creating DataFrame
    df = pd.DataFrame({'Sentence_ID': sentence_ids, 'Org_Sentence': words, 'Org_Tag': tags})

    df_s = df.groupby('Sentence_ID').agg({
        'Org_Sentence': lambda x: ' '.join(x),
        'Org_Tag': lambda x: ' '.join(x)
        }).reset_index()

    # df_s = df_s.rename(columns={"Word": "Org_Sentence"})

    
    df_s['Result'] = df_s['Org_Sentence'].apply(process_sentence)
    df_s[['Sentence', 'Tag']] = pd.DataFrame(df_s['Result'].tolist(), index=df_s.index)
    df_s['Sentence'] = df_s['Sentence'].apply(lambda x: ' '.join(x))
    df_s['Tag'] = df_s['Tag'].apply(lambda x: ' '.join(x))
    # drop results column
    df_s = df_s.drop(columns=['Result'])

    df_s = drop_duplicates(df_s)
    
    # save to csv
    df_s.to_csv(f'data/processed/phee/ace/{file_name}.csv', index=False)

    return df_s

for file_name in files:
    preprocess(file_name)




