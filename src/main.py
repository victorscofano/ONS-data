from src.extract import extract_csv
from src.consolidate import consolidate
from src.load import load
import glob

def main():
    """
    Responsável pela orquestração do pipeline.
    
    => Funções:

            - consolidate()
                Responsável por consolidar os arquivos .csv em apenas um dataframe.
            
            - load()
                Responsável por carregar os arquivos consolidados no banco de dados.
        
            - glob()
                Responsável por procurar todos os arquivos que combinam com o padrão dos diretórios/arquivos.
            
            - sorted()
                Responsável por garantir a ordem cronológica.
    """

    # carrega os arquivos de carga diária
    caminhos_carga = sorted(glob.glob("data/raw/CARGA_ENERGIA_*.csv"))
    df_carga = consolidate(caminhos_carga)
    load(df_carga, "data/processed/database.db", "carga_consolidada")

    # carrega os arquivos de balanço dos subsistemas
    caminhos_balanco = sorted(glob.glob("data/raw/BALANCO_ENERGIA_SUBSISTEMA_*.csv"))
    df_balanco = consolidate(caminhos_balanco)
    load(df_balanco, "data/processed/database.db", "balanco_consolidado")

    # carrega os arquivos de EAR diario dos subsistemas
    caminhos_ear =sorted(glob.glob("data/raw/EAR_DIARIO_SUBSISTEMA_*.csv"))
    df_ear = consolidate(caminhos_ear)
    load(df_ear, "data/processed/database.db", "ear_consolidado")

    # carrega os arquivos de ENA diario dos subsistemas
    caminhos_ena =sorted(glob.glob("data/raw/ENA_DIARIO_SUBSISTEMA_*.csv"))
    df_ena = consolidate(caminhos_ena)
    load(df_ena, "data/processed/database.db", "ena_consolidado")

    # carrega os arquivos de Intercâmbio dos subsistemas
    caminhos_intercamb =sorted(glob.glob("data/raw/INTERCAMBIO_NACIONAL_*.csv"))
    df_intercamb = consolidate(caminhos_intercamb)
    load(df_intercamb, "data/processed/database.db", "intercambio_consolidado")

    # carrega os arquivos de CMO dos subsistemas
    caminhos_cmo = sorted(glob.glob("data/raw/CMO_SEMANAL_*.csv"))
    df_cmo = consolidate(caminhos_cmo)
    load(df_cmo, "data/processed/database.db", "cmo_consolidado")

if __name__ == "__main__":
    main()