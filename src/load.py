from src.consolidate import consolidate
import sqlite3

def load(df, db_caminho: str, table_name: str):
    """
    Responsável por carregar os arquivos no banco de dados.

    => Variáveis:
        - df:
            dataframe que contém os dados do arquivo.
        
        - db_caminho:
            caminho do banco de dados.
        
        - conn:
            faz a conexão do sqlite.

        - table_name:
            recebe o nome da tabela a ser gerada.
    """

    conn = sqlite3.connect(db_caminho)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()