from src.extract import extract_csv
import pandas as pd

def consolidate(caminhos: list[str]):

    """
    Consolida os dados extraídos num dataframe final.

        - caminhos:
            lista de caminhos dos arquivos.
        
        - dfs:
            recebe os dados extraídos de cada arquivo (para cada caminho dentro de caminhos).
            
        - df_final:
            concatena a lista e transforma no dataframe final.
    """

    dfs = [extract_csv(c) for c in caminhos]
    df_final = pd.concat(dfs, ignore_index=True)
    return df_final
    

