"""
📁 ORGANIZADOR AUTOMÁTICO DE ARQUIVOS
Script que organiza automaticamente arquivos em pastas por tipo
"""

import os
import shutil
from pathlib import Path

def organizar_arquivos(pasta_origem):
    """
    Organiza arquivos em pastas por extensão
    
    Args:
        pasta_origem (str): Caminho da pasta para organizar
    
    Returns:
        dict: Relatório com quantos arquivos foram organizados
    """
    # Dicionário com extensões e suas pastas
    categorias = {
        'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Documentos': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
        'Vídeos': ['.mp4', '.mov', '.avi', '.mkv'],
        'Músicas': ['.mp3', '.wav', '.flac'],
        'Scripts': ['.py', '.js', '.html', '.css'],
        'Compactados': ['.zip', '.rar', '.7z']
    }
    
    # Cria as pastas se não existirem
    for categoria in categorias.keys():
        Path(os.path.join(pasta_origem, categoria)).mkdir(exist_ok=True)
    
    # Contador de arquivos movidos
    contador = {categoria: 0 for categoria in categorias.keys()}
    contador['Outros'] = 0
    
    # Percorre todos os arquivos
    for arquivo in os.listdir(pasta_origem):
        caminho_arquivo = os.path.join(pasta_origem, arquivo)
        
        # Ignora se for pasta
        if os.path.isdir(caminho_arquivo):
            continue
        
        # Pega a extensão do arquivo
        _, extensao = os.path.splitext(arquivo)
        extensao = extensao.lower()
        
        # Encontra a categoria
        movido = False
        for categoria, extensoes in categorias.items():
            if extensao in extensoes:
                destino = os.path.join(pasta_origem, categoria, arquivo)
                shutil.move(caminho_arquivo, destino)
                contador[categoria] += 1
                movido = True
                break
        
        # Se não encontrou categoria, vai para "Outros"
        if not movido and extensao:  # Ignora arquivos sem extensão
            Path(os.path.join(pasta_origem, 'Outros')).mkdir(exist_ok=True)
            destino = os.path.join(pasta_origem, 'Outros', arquivo)
            shutil.move(caminho_arquivo, destino)
            contador['Outros'] += 1
    
    # Gera relatório
    print("✅ Organização concluída!")
    print("\n📊 Relatório:")
    for categoria, quantidade in contador.items():
        if quantidade > 0:
            print(f"  {categoria}: {quantidade} arquivo(s)")
    
    return contador
