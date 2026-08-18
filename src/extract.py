#%%
import pandas as pd

def extract_csv(caminho: str):
    """
    Extrai os dados do arquivo .csv, passa para o dataframe e retorna ele.
    
        - caminho:
            caminho do diretório onde o arquivo se encontra. 
        
        - df:
            dataframe que contém os dados do arquivo.
    """

    df = pd.read_csv(caminho, sep=";")
    return df

