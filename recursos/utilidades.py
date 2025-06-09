import datetime

def get_timestamp_formatado():
    """
    Pega a data e a hora atuais e retorna como uma string formatada.
    Exemplo de retorno: "09/06/2025 05:40:15"
    """
    agora = datetime.datetime.now()
    # Formata a data e hora no padrão Dia/Mês/Ano Hora:Minuto:Segundo
    timestamp_formatado = agora.strftime("%d/%m/%Y %H:%M:%S")
    return timestamp_formatado
    
