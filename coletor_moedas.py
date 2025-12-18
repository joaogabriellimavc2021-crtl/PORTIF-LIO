"""
💱 COLETOR DE COTAÇÃO DE MOEDAS
Script que coleta cotações em tempo real e salva em Excel
"""

import requests
import pandas as pd
from datetime import datetime
import os

def coletar_cotacoes():
    """
    Coleta cotações de EUR, USD, GBP em tempo real
    """
    print("📈 Coletando cotações de moedas...")
    
    try:
        # API gratuita para cotações (funciona sem chave)
        url = "https://api.exchangerate-api.com/v4/latest/BRL"
        resposta = requests.get(url, timeout=10)
        dados = resposta.json()
        
        # Extrai as moedas que nos interessam
        moedas_interesse = ['USD', 'EUR', 'GBP', 'ARS', 'CLP']
        cotacoes = {}
        
        for moeda in moedas_interesse:
            if moeda in dados['rates']:
                # 1 moeda estrangeira = X reais
                # Queremos: 1 real = X moeda estrangeira
                cotacoes[moeda] = 1 / dados['rates'][moeda]
        
        # Cria DataFrame
        df = pd.DataFrame({
            'Moeda': list(cotacoes.keys()),
            'Valor_por_1_BRL': list(cotacoes.values()),
            'Data_Hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Formata os valores
        df['Valor_por_1_BRL'] = df['Valor_por_1_BRL'].round(4)
        
        # Salva em Excel
        arquivo_excel = 'cotacoes_moedas.xlsx'
        
        # Se o arquivo já existe, adiciona nova linha
        if os.path.exists(arquivo_excel):
            df_existente = pd.read_excel(arquivo_excel)
            df_completo = pd.concat([df_existente, df], ignore_index=True)
        else:
            df_completo = df
        
        df_completo.to_excel(arquivo_excel, index=False)
        
        print(f"✅ Cotações salvas em '{arquivo_excel}'")
        print("\n💱 Cotações atuais (1 BRL = X moeda):")
        for _, row in df.iterrows():
            print(f"  {row['Moeda']}: {row['Valor_por_1_BRL']}")
        
        return df
    
    except Exception as e:
        print(f"❌ Erro ao coletar cotações: {e}")
        
        # Dados de exemplo em caso de falha
        print("\n⚠️ Usando dados de exemplo...")
        dados_exemplo = {
            'Moeda': ['USD', 'EUR', 'GBP'],
            'Valor_por_1_BRL': [0.19, 0.18, 0.15],
            'Data_Hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return pd.DataFrame(dados_exemplo)

