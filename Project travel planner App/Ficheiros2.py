import json

def salvar_dados(novo_dado):
    """Adiciona novos dados ao fiheiro JSON, acumulando com os dados existentes."""
    try:
        with open('dados.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)  # Carrega os dados existentes
    except FileNotFoundError:
        dados = []  # Se não existir ficheiro, cria uma lista vazia

    dados.append(novo_dado)  # Adiciona o novo dado à lista de dados

    with open('dados.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def carregar_dados():
    """Carrega os dados de um ficheiro JSON."""
    try:
        with open('dados.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []  # Retorna uma lista vazia se o ficheiro não existir