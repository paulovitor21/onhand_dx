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

    return df_onhand
