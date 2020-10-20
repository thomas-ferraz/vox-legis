import pandas as pd 
import numpy as np

def main():

    df = pd.read_csv('dados_pdf_falencias.csv')

    df = df.replace({'tipo_documento': r'Documento[s]* ([0-9]*|Diversos).+'}, {'tipo_documento': 'Documento'}, regex=True)
    df = df.replace({'tipo_documento': r'Documentos'}, {'tipo_documento': 'Documento'}, regex=True)
    df = df.replace({'tipo_documento': r'.+Ofício.+'}, {'tipo_documento': 'Ofício'}, regex=True)
    df = df.replace({'tipo_documento': r'Ofício Recebido' }, {'tipo_documento': 'Ofício'}, regex=True)
    df = df.replace({'tipo_documento': r'Ofícios'}, {'tipo_documento': 'Ofício'}, regex=True)
    df = df.replace({'tipo_documento': r'^([Aa]córdão[s]*.+)'}, {'tipo_documento': 'Acórdão'}, regex=True)
    df = df.replace({'tipo_documento': r'^(Certid[ãõ][oe]s*.+)'}, {'tipo_documento': 'Certidão'}, regex=True)
    df = df.replace({'tipo_documento': r'^(Petiç[ãõ][oe]s*.+)'}, {'tipo_documento': 'Certidão'}, regex=True)
    df = df.replace({'tipo_documento': r'Sentença[s]*'}, {'tipo_documento': 'Senteças'}, regex=True)

    df['tipo_documento'].value_counts().to_csv('docs_type.csv')

    df.to_csv('2_dados_pdf_falencias.csv', index=False)

    #df = pd.read_csv('2_dados_pdf_falencias.csv')

    dates = []
    signers = []
    for index, row in df.iterrows():
        pdf_string = df.iloc[index]['string']
        pdf_string = pdf_string.lower()

        '''
        Tries to find the signature date 
        '''
        data_doc = ''
        index_date = pdf_string.find("protocolado em")
        if index_date != -1:
            data_doc = pdf_string[index_date+15:index_date+25]
        else: 
            index_date = pdf_string.find("liberado nos autos em")
            if index_date != -1: 
                data_doc = pdf_string[index_date+22:index_date+32]

        '''
        Tries to find who has signed the documento
        '''
        nome_assinador = ''
        index_name = pdf_string.find("assinado digitalmente por")
        if index_name != -1:
            index_end_name = pdf_string[index_name:].find(',')
            if index_end_name != -1:
                nome_assinador = pdf_string[index_name+26:index_name+index_end_name]
            else:
                nome_assinador = pdf_string[index_name+26:index_name+106]

        dates.append(data_doc)
        signers.append(nome_assinador)

    df['data_doc'] = dates
    df['nome_assinador'] = signers

    df.to_csv('3_dados_pdf_falencias.csv', index=False)
if __name__ == "__main__":
    main()