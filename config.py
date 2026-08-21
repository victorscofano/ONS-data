from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
RAW_DIR = DATA_DIR / "raw"
QUERIES_DIR = BASE_DIR / "queries_teste"

DATABASE_PATH = PROCESSED_DIR / "database.db"

QUERY_CARGA_MEDIA = "01_media_diaria.sql"
QUERY_CARGA_MAXIMA = "02_maior_carga_diaria.sql"
QUERY_UTIL_FIM_SEMANA = "03_util_fim_de_semana.sql"
QUERY_MEDIA_MENSAL = "04_media_mensal_ano.sql"
QUERY_PERCENT_MEDIA = "05_media_percent_por_fonte.sql"
QUERY_PERCENT_MAIOR_E_MENOR = "06_maior_e_menor_percent_mes.sql"
QUERY_BALANCO_CARGA = "07_comparacao_balanco_carga.sql"
QUERY_ENA_EAR = "08.sql"
QUERY_INTERCAMBIO = "09.sql"