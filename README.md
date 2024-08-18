# Transformer-based Text Highlighting for Medical Terms

This repository contains the implementation of the major research project titled **"Transformer-based Text Highlighting for Medical Terms"**. The study focuses on using transformer models to enhance the efficiency of medical professionals by automatically highlighting key medical terms in texts, aiding in quicker and more accurate information retrieval.

## Table of Contents

- [Introduction](#introduction)
- [Datasets](#datasets)
- [Models](#models)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

The use of technology in healthcare has become increasingly important, especially with the rise of telemedicine and the need for efficient data processing. This project addresses the challenge of information overload in medical documents by implementing transformer-based models for text highlighting. The goal is to enable healthcare professionals to quickly pinpoint important information within large volumes of text.

## Datasets

This project uses the following datasets:

1. **PHEE-6 Dataset**: Adapted from the PHEE dataset, designed for pharmacovigilance, and modified to suit the objectives of medical text highlighting.
2. **PHEE-2 Dataset**: A binary-labeled version of the PHEE-6 dataset.
3. **Medical Chat Dataset**: Comprises doctor-patient dialogues provided by a telemedicine company, used for evaluation purposes.
4. **MTSamples Dataset**: A collection of transcription reports from various specialties, annotated for the text highlighting task.

## Models

The repository includes implementations of the following models:

- **BERT**: Fine-tuned for Named Entity Recognition (NER) tasks in medical text.
- **DeBERTa**: Enhanced BERT model with improved contextual understanding.
- **BioBERT**: Pre-trained on biomedical literature for high accuracy in medical NER tasks.
- **SciBERT**: Trained on scientific papers, including biomedical literature.
- **BERT-Clinical**: Specifically fine-tuned for identifying Problem, Test, and Treatment categories in medical texts.
- **BioClinicalBERT**: Pre-trained on electronic health records for accurate identification of medical entities.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lara-ozyegen/MRP_MedHighlight.git
   cd MRP_MedHighlight

## Usage

The BERT-finetuning and adaptive fine-tuning codes can be found under the `notebooks` directory.

- **BERT-CRF**: A combination of BERT and Conditional Random Fields (CRF) for enhanced sequence prediction. The implementation used in this project is available [here](https://github.com/shushanxingzhe/transformers_ner).
- **ACE (Automated Concatenation of Embeddings)**: Integrates multiple embedding representations of text for optimized word embedding. The code used for ACE in this project is available [here](https://github.com/Alibaba-NLP/ACE).
- **Unsupervised Learning**: Utilizes the unlabeled MTSamples dataset. The code is available [here](https://github.com/UKPLab/sentence-transformers/tree/master/examples/unsupervised_learning/MLM).

