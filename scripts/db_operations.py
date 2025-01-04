from sqlalchemy.orm import Session
from scripts.models import OnhandRecord
from scripts.generate_hash import generate_hash
from scripts.generate_hash import generate_hash


def save_to_db(df_onhand, db: Session, file_date):
    """
    Salva os registros no banco de dados usando ORM.
    Processa todos os registros, mas apenas os registros não duplicados serão inseridos no banco.

    Args:
        df_pph (DataFrame): DataFrame com os dados a serem inseridos.
        db (Session): Sessão do banco de dados.
    """

    # hash para chave unica
    # Passo 1: Criar uma coluna 'temp_id' no DataFrame com números crescentes
    df_onhand['temp_id'] = range(1, len(df_onhand) + 1)

    # Passo 2: Gerar o hash baseado na combinação das colunas
    df_onhand['hash_id'] = df_onhand.apply(
            lambda row: generate_hash(row['temp_id']),
        axis=1
    )
    duplicate_count = 0  # Contador para duplicados
    inserted_count = 0  # Contador para registros inseridos
    for _, row in df_onhand.iterrows():
        # Verificar se o hash já existe no banco
        exists = db.query(OnhandRecord).filter_by(hash_id=row['hash_id']).first()

        if exists:
            duplicate_count += 1  # Incrementa o contador de duplicados
            print(f"[Duplicado] Registro já existe para hash: {row['hash_id']}. Ignorando este registro.")
            continue  # Ignora a inserção do registro duplicado, mas continua processando os próximos

        # Se não for duplicado, criar e adicionar o novo registro
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
            purchaser = row['Purchaser'],
            hash_id=row['hash_id']  # Usando o hash_id gerado
        )
        db.add(record)
        inserted_count += 1  # Incrementa o contador de registros inseridos

    # Commit no banco
    db.commit()
    # Exibe a quantidade de duplicados encontrados
    print(f"Total de duplicados encontrados: {duplicate_count}")
    print(f"Total de registros não duplicados inseridos: {inserted_count}")
    print("[Inserido] Todos os registros não duplicados foram inseridos com sucesso.")