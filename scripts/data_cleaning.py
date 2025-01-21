import pandas as pd

def clean_data(df_onhand: pd.DataFrame) -> pd.DataFrame:
    """Limpa e transforma os dados para adequação ao modelo.

    Args:
        engine: Conexão ao banco de dados.
        df_delivery_status (pd.DataFrame): Dados a serem limpos.

    Returns:
        pd.DataFrame: Dados limpos e transformados.
    """
    
    # manter as colunas
    columns_to_keep = [
        'ORG',
        'Item',
        'UIT', 
        'Desc', 
        'Subinv',
        'Locator',
        'Onhand Qty',
        'Planner',
        'Purchaser']

    df_onhand = df_onhand[columns_to_keep]

    # Garantir que a coluna "Planner" é string
    df_onhand['Planner'] = df_onhand['Planner'].astype(str)
    df_onhand['Purchaser'] = df_onhand['Purchaser'].astype(str)

    # Dicionário de palavras-chave para categorias
    category_map = {
        'CLAIM': ['DEF', 'CLAIM', 'CONTROL', 'SCRAP', 'FUM', 'DIV', 'DEV', 'IQC', 'SCR', 'SQA', 'PRO', 'LOS', 'EOL', 'RMA', 'R&D', 'REJ', 'REW', 'RET', 'TOM', 'REP', 'NG', 'FU_'],
        'MTL': ['MTL', 'CONREC', 'CONT', 'FAC', 'W/H', 'WH', 'CANOPY'],
        'FA': ['WIP', 'ASSY', 'EMS', 'MISP', 'MB'],
        'Interno': ['PCB', 'CTBOX', 'REMOC', 'INJ', 'SUB', 'BRACK', 'HE'],
        'OSP': ['PASTD', 'QUALE', 'TSE', 'TUTI', 'TOMAM', 'SATO', 'PNL', 'TYANG', 'FLEXE', 'VENTTN', 'VENTTO']
    }

    def determine_material_type_identifier(row):
        # Verificar correspondência nas categorias do dicionário
        for category, keywords in category_map.items():
            if any(keyword in row['Subinv'] or keyword in row['Locator'] for keyword in keywords):
                if category == 'CLAIM':
                    return category
                else:
                    return category + str(row['Item']) + str(row['UIT'])
        return "Others"  # Caso não encontre nenhuma correspondência
    
    # Aplicando a função ao DataFrame para criar a coluna 'Material_Type_Identifier'
    df_onhand['Material_Type_Identifier'] = df_onhand.apply(determine_material_type_identifier, axis=1)

    return df_onhand
