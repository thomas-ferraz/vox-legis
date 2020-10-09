# Processing the Datasets

## dataset1

The dataset1 for "falências" and "recuperações judiciais" provides R-objects (.rds files) for each process, containing its number, the complete page with administrative data from the e-SAJ (complete HTML, style and javascript code) and a flag indicating if it is a digital process. 

### import_rdata

The notebook requires:
- RPy2
- Pandas

It loads the dataset and saves the R-object data in a csv file, for easier handling and portability.

### extract_html

The notebook requires:
- Beautiful Soup
- Pandas

It loads the csv generated with import_rdata.ipynb and extracts relevant information about the process's into a Pandas DataFrame, saving in a csv.

| num_proc | status | juiz | terceiros | rep_legal | valor_acao | reqte | adv_reqte | reqdo | adv_reqdo |
| -------- | ------ | ---- | --------- | --------- | ---------- | ----- | --------- | ----- | --------- |

## dataset2

The dataset2 for "falências" provides zip files containing pdf with all the information about the process's.

### unzip
The notebook unzips all files in another directory, using the same structure as the original.

### extract_pdf
The notebook requires:
- Textract

It loads each pdf file for each process, extracting relevant information and saves it in a csv file. This is the most time intensive part of the information retrieval process so far.

| n_processo_ | tipo_documento | string | data_doc | assinado_por | n_folha_inicio | n_folha_fim |
| ----------- | -------------- | ------ | -------- | ------------ | -------------- | ----------- |
