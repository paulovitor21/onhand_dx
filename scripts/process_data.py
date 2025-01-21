import os
import logging
from scripts.db_connection import SessionLocal, engine
from scripts.models import Base
from scripts.data_loader import load_excel
from scripts.data_cleaning import clean_data
from scripts.db_operations import save_to_db
from scripts.extract_data_file import extrair_data
import pandas as pd
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extrair_data(xlsb_file):
    data_criacao = os.path.getmtime(xlsb_file)
    data_criacao_formatada = datetime.fromtimestamp(data_criacao).strftime('%Y-%m-%d %H:%M:%S')
    return data_criacao_formatada

def processa_arquivo(xlsx_file):
    # Cria as tabelas no banco de dados
    Base.metadata.create_all(bind=engine)

    # Criar sessão
    db = SessionLocal()
    
    try:
        # Carregar os dados
        with pd.ExcelFile(xlsx_file) as xls:
            df_onhand = xls.parse()

        # Extrair data do arquivo
        file_date = extrair_data(xlsx_file)
        logging.info(f"Data do ARQUIVO -> {file_date}")
        
        # Limpar os dados
        df_onhand = clean_data(df_onhand)
        
        # Salvar no banco
        save_to_db(df_onhand, db, file_date)
    except Exception as e:
        logging.error(f"Ocorreu um erro na execução do processo: {e}")
        logging.exception("Detalhes do erro: ")
    finally:
        # Deletar o arquivo convertido para evitar acúmulo
        if xlsx_file and os.path.exists(xlsx_file):
            try:
                os.remove(xlsx_file)
                logging.info(f"Arquivo temporário removido: {xlsx_file}")
            except Exception as e:
                logging.error(f"Não foi possível excluir o arquivo: {e}")

        # Fechar conexão com o banco de dados
        db.close()