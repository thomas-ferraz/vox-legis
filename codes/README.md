## Introduction

The Jupyter Notebooks presented are responsible for:
- Data extraction;
- Pre-processing;
- Data analysis;
- Feature extraction;
- Annotation;
- Modeling.

## Dataset

The data is provided in 2 datasets (dataset1 and dataset2) with "falências" and "recuperações judiciais" processes. Data extraction was made in both, but further work focussed only in the "falências" processes.

# Data Extraction

This step extracts text data from the files provided and stores it in .csv files in multiple stages, allowing simpler processing of data and portability. Each step creates a csv that may be needed for other code, so there is an order to the extraction.

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

# Pre-processing

- classify_decisions.ipynb

Provides data cleansing.

## classify_decisions

The notebook requires:
- nltk
- Pandas
- Numpy
- Seaborn
- Matplotlib
- Gensim
- SciKitLearn

# Data Analysis

- clusters_pdf.ipynb
- descriptive_statistics.ipynb
- extract_bigrams.py

Provides some analysis needed to expand knowledge of the data.

## descriptive_statistics

The notebook requires:

## decriptive_stats

The notebook requires:

# Annotation & Modeling

- classify_decisions.ipynb 

The requirements were previously presented. 