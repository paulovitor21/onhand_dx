# main.py
import logging
from scripts.process_data import processa_arquivo
def main():
    
    try:
        # Carregar os dados
        xlsx_file = r"Integration Onhand Inquiry20250113.xlsx"

        # processar arquivo
        processa_arquivo(xlsx_file)
    except Exception as e:
        logging.error(f"Ocorreu um erro na execução do processo: {e}")
        logging.exception("Detalhes do erro: ")

if __name__ == "__main__":
    main()