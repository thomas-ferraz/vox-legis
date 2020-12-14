## Introduction

The Jupyter Notebooks presented are responsible for:
- Data extraction;
- Pre-processing;
- Data analysis;
- Feature extraction;
- Annotation;
- Modeling.

This document provides a overview of each notebook, allowing a user to check where it needs to execute the code to obtain the data or information needed.

## Dataset

The data is provided in 2 datasets (dataset1 and dataset2) with "falências" and "recuperações judiciais" procedures. Data extraction was made in both, but further work focussed only in the "falências" data.

# Data Extraction

This step extracts text data from the files provided and stores it in .csv files in multiple stages, allowing simpler processing of data and portability. Each step creates a csv that may be needed for other code, so there is an order to the extraction.

# Utils

Using Google Collab/Drive with GitLab as a development tools requires the repo to be in Google Drive and commands to be run from Google Colab. A notebook provides a tutorial setting up the environment:

- commit_from_google_colab.ipynb

## dataset1

- extract_rds.ipynb
- extract_html.ipynb

The dataset1 for "falências" and "recuperações judiciais" provides R-objects (.rds files) for each process, containing its number, the complete page with administrative data from the e-SAJ (complete HTML, style and javascript code) and a flag indicating if it is a digital process.

### extract_rds

The notebook requires:
- RPy2
- Pandas
- dataset1 - .rds files

Loads all the .rds files from dataset and extracts the R-object data to a csv file - ``falencias.csv`` and ``recuperacoes_judiciais.csv``

### extract_html

The notebook requires:
- Beautiful Soup
- Pandas
- ``falencias.csv`` and ``recuperacoes_judiciais.csv`` from extract_rds

Loads the previously generated .csv files and extracts relevant information about the processes into a Pandas DataFrame, and writes it in a csv - ``falencias_html.csv`` and ``recuperacoes_judiciais_html.csv`` - with the head:

| num_proc | status | juiz | terceiros | rep_legal | valor_acao | reqte | adv_reqte | reqdo | adv_reqdo |
| -------- | ------ | ---- | --------- | --------- | ---------- | ----- | --------- | ----- | --------- |

## dataset2

- extract_unzip.ipynb
- extract_pdf.ipynb

The dataset2 for "falências" provides zip files containing pdf files with all the information about the processes. This extraction exceeds some I/O limitations present even in the unlimited Google Drive and Google Collab platforms, thus it is recommended to be run locally.

### extract_unzip

The notebook requires:
- .zip files of the dataset2 (about 120GB of data)

The Notebook unzips all files in another directory, keeping the same file structure as the original.

### extract_pdf

The notebook requires:
- Textract
- .pdf files extracted by extract_unzip (about 140GB of data)

Loads each pdf file for each process, extracting relevant information and writing it in a csv file - ``dados_pdf_falencias.csv`` (about 1.5GB) - with the header:

| n_processo_ | tipo_documento | string | data_doc | assinado_por | n_folha_inicio | n_folha_fim |
| ----------- | -------------- | ------ | -------- | ------------ | -------------- | ----------- |

At this point, work focussed in the data provided in ``dados_pdf_falencias.csv``, and experiments and advancements were made based on it.

# Pre-processing

- classify_decisions.ipynb

Provides data cleansing and further reduction of the dataset. The notebook is also responsible for annotation and modeling, explained further in this document.

## classify_decisions

The notebook requires:
- NLTK
- Pandas
- Numpy
- Seaborn
- Matplotlib
- Gensim
- scikit-learn

Loads the file ``dados_pdf_falencias.csv``, standardizes document types, extracts signatures and its dates, reduces the data to contain only documents written by a judge.
# Data Analysis

- clusters_pdf.ipynb
- descriptive_statistics.ipynb
- extract_bigrams.py

Provides some analysis needed to expand knowledge of the data, and the exploratory data analysis required during the course. Those are mostly graphs and images, with some exploration of tools such as clustering and embeddings of the data.

## clusters_pdf

The notebook requires:
- Pandas
- Numpy
- Seaborn
- Matplotlib
- NLTK
- top2vec
- hdbscan
- Joblib
- scikit-learn
- umap
- SciPy
- dbmap
- Gensim

## descriptive_statistics

The notebook requires:
- Pandas
- Numpy
- Seaborn
- Matplotlib
- WordCloud
- NLTK
- spaCy

## extract_bigrams

The notebook requires:
- Pandas
- Numpy
- NLTK
# Annotation & Modeling

- classify_decisions.ipynb 

The requirements were previously presented.

With ``dados_pdf_falencias.csv`` as input, the notebook proceeds with cleansing and reduction, as mentioned, and removes control characters and stopwords. A fraction of the reduced dataset is labelled using REGEX and all of it is embedded with Doc2Vec, enabling a neural network to classify and train the data, providing a model for evaluation.

