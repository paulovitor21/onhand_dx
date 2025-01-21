from sqlalchemy.orm import Session
from scripts.models import OnhandRecord
from scripts.generate_hash import generate_hash
from scripts.generate_hash import generate_hash
import logging

def save_to_db(df_onhand, db: Session, file_date):
    """
    Salva os registros no banco de dados usando ORM.
    Processa todos os registros, mas apenas os registros não duplicados serão inseridos no banco.

    Args:
        df_pph (DataFrame): DataFrame com os dados a serem inseridos.
        db (Session): Sessão do banco de dados.
    """
    # Verificar se já existem registros no banco para a mesma data do arquivo
    existing_records = db.query(OnhandRecord).filter_by(file_date=file_date).first()
    
    if existing_records:
        logging.info(f"[Ignorado] Registros para a data {file_date} já existem no banco. Nenhum registro foi inserido.")
        return False  # Nenhum dado foi inserido
    
    # Inserir os registros, pois não existem registros para a data do arquivo
    inserted_count = 0

    for _, row in df_onhand.iterrows():
        
        record = OnhandRecord(
            file_date = file_date,
            org = row['ORG'],
            item = row['Item'],
            uit = row['UIT'],
            desc = row['Desc'],
            subinv = row['Subinv'],
            locator = row['Locator'],
            onhand_qty = row['Onhand Qty'],
            planner = row['Planner'],
            purchaser = row['Purchaser']
        )
        db.add(record)
        inserted_count += 1  # Incrementa o contador de registros inseridos

    # Commit no banco
    db.commit()
    # Exibir mensagem de sucesso apenas se registros forem inseridos
    logging.info(f"[Inserido] Total de registros inseridos para a data {file_date}: {inserted_count}.")
    logging.info("Dados salvos com sucesso!")
    return True