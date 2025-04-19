import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def obter_dados_completos_para_data(data_desejada, csv_file='dados_hidrometeorologicos.csv'):
    df = pd.read_csv(csv_file)
    data_formatada = datetime.strptime(data_desejada, "%d-%m-%Y").strftime("%d/%m/%Y")
    
    if data_formatada not in df["Data"].values:
        raise ValueError("Data não encontrada nos dados.")
    
    dados = df[df["Data"] == data_formatada].iloc[0]
    dias = [(datetime.strptime(data_formatada, "%d/%m/%Y") + timedelta(days=i)).strftime("%d/%m") for i in range(7)]

    erro = np.array([0.0716, 0.1064, 0.1282, 0.1402, 0.1843, 0.199, 0.21])
    atencao = [560] * 7
    alerta = [620] * 7

    previsao = dados[['Cota_Atual_Prevista', 'Previsao_D1', 'Previsao_D2', 'Previsao_D3', 'Previsao_D4', 'Previsao_D5', 'Previsao_D6']].values.astype(float)
    cotas_reais = dados[['Cota_Real_Atual', 'Cota_Real_D1', 'Cota_Real_D2', 'Cota_Real_D3', 'Cota_Real_D4', 'Cota_Real_D5', 'Cota_Real_D6']].values.astype(float)

    previsao_mais = (previsao * (1 + erro)).tolist()
    previsao_menos = (previsao * (1 - erro)).tolist()

    parametros = {
        "Quipapá Pluviométrico": dados['Quipapa_Pluviometria'],
        "São Benedito do Sul Pluviométrico": dados['Sao_Benedito_Sul_Pluviometria'],
        "São Benedito do Sul Fluviométrico": dados['Sao_Benedito_Sul_Fluviometria'],
        "Batateira Fluviométrico": dados['Batateira_Fluviometria'],
        "Belém de Maria Pluviométrico": dados['Belem_Maria_Pluviometria'],
        "Belém de Maria Fluviométrico": dados['Belem_Maria_Fluviometria'],
        "Maraial Pluviométrico": dados['Maraial_Pluviometria'],
        "Jaqueira Pluviométrico": dados['Jaqueira_Pluviometria'],
        "Laje Grande Pluviométrico": dados['Laje_Grande_Pluviometria'],
        "Catende Pluviométrico": dados['Catende_Pluviometria'],
        "Catende Fluviométrico": dados['Catende_Fluviometria'],
        "Palmares Pluviométrico 1": dados['Palmares_Pluviometria_1'],
        "Palmares Pluviométrico 2": dados['Palmares_Pluviometria_2'],
    }

    return {
        "dias": dias,
        "cotas_reais": cotas_reais.tolist(),
        "previsao": previsao.tolist(),
        "previsao_mais": previsao_mais,
        "previsao_menos": previsao_menos,
        "atencao": atencao,
        "alerta": alerta,
        "parametros": parametros
    }

def listar_datas(csv_file='dados_hidrometeorologicos.csv'):
    df = pd.read_csv(csv_file)
    return sorted(df["Data"].unique())
