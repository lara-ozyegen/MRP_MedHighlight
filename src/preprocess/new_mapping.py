"""
This script maps the tags in the ACE dataset to a smaller set of tags and forms the PHEE-6 dataset.
"""
import pandas as pd
import string

treatment_tags = [
    "I-Treatment.Drug",
    "I-Treatment.Combination.Drug",
    "I-Treatment",
    "I-Treatment.Route",
    "I-Treatment.Dosage",
    "I-Combination.Drug",
    "I-Dosage",
    "I-Drug",
]

# Map to the new tag
treatment_mapping = {tag: "I-Treatment" for tag in treatment_tags}

problem_tags = [
    "I-Effect",
    "I-Treat_Disorder",
    "I-Treatment.Treat_Disorder",
    "I-Subject.Sub_Disorder",
    "I-Sub_Disorder"
]

# Map to the new tag
problem_mapping = {tag: "I-Problem" for tag in problem_tags}

background_tags = [
    "I-Subject.Age",
    "I-Subject.Gender",
    "I-Subject.Race",
    "I-Subject",
    "I-Race",
    "I-Gender"
]

# Map to the new tag
background_mapping = {tag: "I-Background" for tag in background_tags}

other_tags = [
    "I-Duration",
    "I-Time_elapsed",
    "I-Freq",
    "I-Treatment.Time_elapsed",
    "I-Treatment.Freq",
    "I-Treatment.Duration"
]

# Map to the new tag
other_mapping = {tag: "I-Other" for tag in other_tags}

o_tags = [
    "I-Subject.Population",
    "I-Potential_therapeutic_event.Trigger",
    "I-Adverse_event.Trigger",
    "I-Route",
    "I-Population",
    "O"
]

# Map to the new tag
o_mapping = {tag: "O" for tag in o_tags}

test_tags = [
    "I-Test"
]

test_mapping = {tag: "I-Test" for tag in test_tags}

# Combine all mappings
all_mappings = {**treatment_mapping, **problem_mapping, **background_mapping, **other_mapping, **o_mapping, **test_mapping}

def map_tags(tag_string):
    return ' '.join(all_mappings.get(tag, tag) for tag in tag_string.split())

# List of words to relabel as "O"
words_to_relabel = ["a", "an", "and", "the", "with", 'for', 'nor', 'but', 'or', 'yet', "to", "of", "on", "in", "patient", "history", "patients", "as", "she", "he", "his", "her"]
modified_punctuation = string.punctuation.replace('-', '') # do not ignore '-' in 55-year-old

# Function to change the label of specific words to "O"
def relabel_words(row):
    words = row['sentence'].split()
    tags = row['tag'].split()
    new_tags = []

    for word, tag in zip(words, tags):
        if word.lower() in words_to_relabel or word in modified_punctuation:
            new_tags.append('O')
        else:
            new_tags.append(tag)
    
    return ' '.join(new_tags)

files = ['train', 'dev', 'test']
for file_name in files:
    df_w_t = pd.read_csv(f'data/processed/phee/ace/{file_name}_w_test_tag.csv')
    df_w_t["Med_Tag"] = df_w_t["Org_Tokenized_Tag"].apply(map_tags)
    df_w_t = df_w_t[['Sentence', 'Med_Tag']]
    df_w_t.rename(columns={"Sentence": "sentence", "Med_Tag": "tag"}, inplace=True)

    # relabel punctuation and conjunctions as "O"
    df_w_t['tag'] = df_w_t.apply(relabel_words, axis=1)

    # save to csv
    df_w_t.to_csv(f'data/processed/phee/ace/{file_name}_w_test_tag_new_mapped.csv', index=False)



