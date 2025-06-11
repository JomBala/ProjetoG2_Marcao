import json
import os

from recursos.utilidades import get_timestamp_formatado

def registrar_partida(player_name, pontos):
    
    # Registra a pontuação, nome e o timestamp em log.dat.

    timestamp = get_timestamp_formatado()
    log_entry = {
        "nome": player_name,
        "pontos": pontos,
        "timestamp": timestamp
    }
    
    logs = [] 
    
    # Verifica se o ficheiro log.dat existe e lê os dados
    
    if os.path.exists("log.dat"):
        try:
            if os.path.getsize("log.dat") > 0:
                with open("log.dat", "r", encoding="utf-8") as f:
                    dados_carregados = json.load(f)
                    if isinstance(dados_carregados, list):
                        logs = dados_carregados
        except (json.JSONDecodeError, FileNotFoundError):
            print("Arquivo de log corrompido ou não encontrado. Criando um novo.")
            logs = []

    logs.append(log_entry)
    
    try:
        with open("log.dat", "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao escrever no arquivo de log: {e}")

def obter_ultimos_registros(quantidade=5):
    
    #Lê o log e retorna os últimos 'quantidade' de registros, ordenados por pontos.
    
    logs = []
    if os.path.exists("log.dat"):
        try:
            if os.path.getsize("log.dat") > 0:
                with open("log.dat", "r", encoding="utf-8") as f:
                    dados_carregados = json.load(f)
                    if isinstance(dados_carregados, list):
                        logs = dados_carregados
        except (json.JSONDecodeError, FileNotFoundError):
            return [] 
    
    # Ordena por pontos (maior primeiro) e pega os últimos registros
    ultimos_scores = sorted(logs, key=lambda x: x.get('pontos', 0), reverse=True)[:quantidade]
    return ultimos_scores
